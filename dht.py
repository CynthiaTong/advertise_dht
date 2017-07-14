dy_import_module_symbols("routing.r2py")
dy_import_module_symbols("rpc.r2py")
dy_import_module_symbols("lookup.r2py")
dy_import_module_symbols("storage.r2py")
dy_import_module_symbols("util.r2py")

DHT_EVENT_NONE = 0
DHT_EVENT_VALUES = 1
DHT_EVENT_LOOKUP_DONE = 2

TOKEN_SIZE = 16 


class DHT:

	def __init__(self, s, dht_id): # s - whether we have a socket or not (int, -1/else)
		self.id = dht_id
		self.long_id = string_to_long(self.id)
		self.lookups = None 
		self.storage = None 
		self.router = None 
		self.dht_lookup = DHT_Lookup(self.id)
		self.dht_socket = s 
		self.secret_package = rotate_secret() 

		# bucket_grow_time & confirm_nodes_time for maintenance? 
		# token_bucket_time for rate control?

	def new_message(self, buf, source_ip, source_port, to_sleep, callback=None):

		if len(buf) > 0:
			if self.invalid_address(source_ip, source_port):
				return self.periodic()

			msg = parse_message(buf)
			if msg == -1:
				return self.periodic()

			log (msg, "\n")
			(msg_type, tid, tid_len, sender_id, info_hash, target, port, token, token_len,
			nodes, nodes_len, values, values_len) = msg 

			if msg_type == "ERROR" or string_to_long(sender_id) == 0:
				log ("Faulty message - unparseable: \n", buf, "\n")
				return self.periodic()

			if sender_id == self.id:
				log ("Received message from self. weird.\n")
				return self.periodic()

			## Rate control ?? 

			if msg_type == "REPLY":
				if not tid_len == 4:
					log ("Broken tid:\n", buf, "\n")
					return self.periodic()

				if tid_match(tid, "pn"):
					log ("Pong!\n")
					self.router.add_contact(sender_id, source_ip, source_port, 0) # 0 for reply

				elif tid_match(tid, "gp") or tid_match(tid, "fn"):
					lids = (tid_match(tid, "gp") , tid_match(tid, "fn"))
					# try to find among existing lookups by searching lid 
					for lid in lids:
						if lid:
							lookup = self.lookups.find_lookup_by_tid(lid) 
							log ("Got %d nodes for tid: %s\n" % (nodes_len/26, tid))
							# check nodes_len is normal 
							if not nodes_len % 26 == 0:
								log ("Unexpected length for node info!\n")
							elif lookup == None:
								log ("Unknown lookup!\n")
								self.router.add_contact(sender_id, source_ip, source_port, 1) # 1 for query (msg)
							else: # nodes_len normal & existing lookup - it's a proper reply 
								self.router.add_contact(sender_id, source_ip, source_port, 0) # 0 for reply 
								i = 0 
								while i < nodes_len:
									n = nodes[i:i+26]
									n_id = n[:20]
									n_ip = n[20:24]
									n_port = n[24:]
									i += 26 
									if n_id == self.id:
										continue;
									self.router.add_contact(n_id, n_ip, n_port, 2) # 2 for arbitrary msgs 
									# insert into the corresponding lookup  
									lookup.insert(n_id, n_ip, n_port)
								# since we got a reply, send out another round of lookups 
								self.lookups.lookup_get_peers(lookup)
								lookup.insert(sender_id, source_ip, source_port, 1, token, token_len)

					if values_len > 0 and lid[0]:
						log ("Got %d values!\n" % values_len/6)
						if callback:
							return callback(DHT_EVENT_VALUES, lookup.target_id, values, values_len)

				elif tid_match(tid, "ap"):	
					log ("Got reply to announce_peer!\n")
					lid = tid_match(tid, "ap")
					lookup = self.lookups.find_lookup_by_tid(lid) 
					if lookup == None:
						log ("Unknown lookup!\n")
						self.router.add_contact(sender_id, source_ip, source_port, 1) # 1 for query (msg)
					else:
						self.router.add_contact(sender_id, source_ip, source_port, 0) # 0 for reply 
						for n in lookup:
							if n.id == sender_id:
								n.last_req = 0 
								n.replied = 1 
								n.last_replied = getruntime()
								n.acked = 1 
								n.pinged = 0 
								break 
							self.lookups.lookup_get_peers(lookup)

				else:
					log ("Unexpected reply: \n%s (%d)\n" % buf, len(buf))

			elif msg_type == "PING":
				log ("Ping!\n")
				self.rounter.add_contact(sender_id, source_ip, source_port, 1) # 1 for msg 
				log ("Sending pong.\n")
				self.rpc.pong(source_ip, source_port, tid, tid_len)

			elif msg_type == "FIND_NODE":
				log ("Find node!\n")
				self.rounter.add_contact(sender_id, source_ip, source_port, 1) # 1 for msg 
				log ("Sending closest node to find_node req.\n")
				self.rpc.send_closest_nodes(source_ip, source_port, tid, tid_len, target)

			elif msg_type == "GET_PEERS":
				log ("Get peers!\n")
				self.rounter.add_contact(sender_id, source_ip, source_port, 1) # 1 for msg 
				if string_to_long(info_hash) == 0:
					log ("Got get_peers with no info_hash\n")
					self.rpc.send_error(source_ip, source_port, tid, tid_len, 
															203, "Get_peers with no infohash.")
				else:
					peers_list = self.storage.retrieve(info_hash)
					token = make_token(source_ip, self.secret_package[1])
					if peers_list:
						log ("Sending found peers.\n")
						self.rpc.send_closest_nodes(source_ip, source_port, tid, tid_len, info_hash, 
																				token, TOKEN_SIZE, peers_list)
					else:
						log ("Sending nodes for get_peers.\n")
						self.rpc.send_closest_nodes(source_ip, source_port, tid, tid_len, info_hash)

			elif msg_type == "ANNOUNCE_PEER":
				log ("Announce peer!\n")
				self.rounter.add_contact(sender_id, source_ip, source_port, 1) # 1 for msg 
				if string_to_long(info_hash) == 0:
					log ("Got announce_peer with no info_hash\n")
					self.rpc.send_error(source_ip, source_port, tid, tid_len, 
															203, "Announce_peer with no infohash.")		
				if port == 0:
					log ("Got announce_peer with port 0\n")
					self.rpc.send_error(source_ip, source_port, tid, tid_len, 
															203, "Announce_peer with forbidden port number.")		
				if not token_match(token, source_ip, self.secret_package[0], self.secret_package[1]):
					log ("Got announce_peer with invalid token\n")
					self.rpc.send_error(source_ip, source_port, tid, tid_len, 
															203, "Announce_peer with invalid token.")		
				self.storage.store(sender_id, source_ip, source_port)
				log ("Sending peer announced.\n")
				self.rpc.peer_announced(source_ip, source_port, tid, tid_len)


	def invalid_address(self, ip, port):
		# log (ip, ": ", port, "\n")
		if port == 0 or ip[0] == "0" or ip[:3] == "127" or int(ip[:3]) > 224:
			return True 
		return False 	

	def periodic(self):
		log ("do periodic stuff.\n")
