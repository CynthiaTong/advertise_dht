## Questions 

  - The language to use for the implementation - Python or C? 
  - Use publickey as key and IP Address as value, and SHA-1 Hash? 
  - A bridge between advertise.r2py and the DHT? 
  
## Problems

  - Error when testing advertise.r2py (`advertise_annouce` in specific, the lookup function seems fine) 
  
    Update: centralizedadvertise_v2.r2py works. 
  
    Local error message: 
    
        Exception (with class '.AdvertiseError'): ['announce error (type: central): The connection was refused!'] 
        
    With `Seash`:
    
        An error occurred: Node Manager error 'Unknown Call'
    
## Logical Flow of the project 

  1. Bootstrap and maintain a network 
    
      - Using peer files
      
      - maintainance (call the dht's `dht_periodic` function) 
      
  2. Init the DHT 
  
      call the dht's `dht_init` function
  
  3. Announce (PUT) 
    
  4. Lookup (GET) 
  
      for both announce and lookup, see [KadNode's Implementation](https://github.com/mwarning/KadNode/blob/master/src/kad.c)

  5. Helper & Debug 
    
      print network info, node info, etc. 
  
