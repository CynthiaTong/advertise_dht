## Questions 
      
   - Include additional DHT functionalities, such as [Version Identifier](http://www.bittorrent.org/beps/bep_0005.html) and nodes blacklist? 
   
   
## Problems
   
   - While bootstrapping and the node lookup process, nodes returned by the public bootstrap nodes do not respond to messages.
   
     Possible issues: 
      
     parsing node addresses / message encoding (did some testing and it seems fine),             
     or the nodes themselves 
   
   
## To-dos 

   - Investigate KadNode - how it bootstrap its initial network
   
   - Look at KadNode's advertise and lookup methods, also Seattle's advertise library 
