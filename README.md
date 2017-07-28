## Questions 
   
   - What would the keys be? 
   
      Right now they are randomly generated 20-byte strings; one other way is to sha-1 hash the key value provided by users
   
## Problems

   - Signature verification is done with ed25519, might be hard to implement the algorithm in Repy. 
   
      Existing projects:
      
      [https://github.com/substack/ed25519-supercop](https://github.com/substack/ed25519-supercop)
      
      [https://github.com/warner/python-ed25519](https://github.com/warner/python-ed25519)
      
## To-dos 

   
   - Value reannounce and expire 
   
   - Add peerfile IO
   
   - Unit Testing! 
