## Questions 
   
   - What would the keys be? 
   
      Right now they are randomly generated 20-byte strings; one other way is to sha-1 hash the key value provided by users
      
   - Have PUT and GET support both mutable and immutable data?  See [BEP44](http://www.bittorrent.org/beps/bep_0044.html)
   
## Problems
   
   
## To-dos 

   
   - Look at KadNode's advertise and lookup methods, also Seattle's advertise library. 
     
     Add values methods to reannounce data. 
   
   - Include additional DHT functionalities such as nodes blacklist 
   
   - Add peerfile IO
   
