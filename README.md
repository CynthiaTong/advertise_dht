## Questions 

   - anyway to use either `bytearray` or `struct` in repy? Need them to build RPC messages 
       
   - Bitwise operations to split buckets? 
     
     UPDATE: The [Bittorent DHT Protocol](http://www.bittorrent.org/beps/bep_0005.html) acknowledges splitting by integer          range, though this is different from the Kademlia paper spec. 
   
   - ~~Having "bad node" criteria as Bittorent protocol requires? (jech's dht also does this, but with different time interval  requirements)~~
   
   
## Problems

   - KadNode routing tables keeps buckets in a sorted linked list, problem finding closest buckets? (should use actual Binary      Tree structure? 
     
     UPDATE: The simplest way to find _strictly_ closest nodes is to scan the whole routing table - yet this is unspecified in      the Kademlia paper. Actual implementation will need to depend on the system itself; if a node only stores a couple dozen      contacts, linear scanning is good enough and optimizes the search. Otherwise, the finding-k-closest algorithm seems            pretty involved. 
     ([stackoverflow question](https://stackoverflow.com/questions/30654398/implementing-find-node-on-torrent-kademlia-routing-table)           about this). 
     
   
   - Internal Error while executing routing.r2py: 
   
      ```
      Exception (with class 'socket.error'): [Errno 1] Operation not permitted
      ```

## To-dos 

   - Implement node lookup 
 
   - Implement RPC class 
  
