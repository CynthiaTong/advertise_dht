## Questions 

   - Read publickeys from local .publickey file with `sshkey_file_to_publickey(filename)` and `rsa_publickey_to_string(publickey)` ?

## Problems

  - Error dylinking sshkey.r2py 
  
    Local error message: 
    
        Failed to initialize the module (sshkey_paramiko.r2py)! Got the following exception: 
        'CodeUnsafeError('Code failed safety check! Error: (\'<class \\\'exception_hierarchy.CheckStrException\\\'> 
        ("Unsafe string \\\'decode\\\' in line 98, node attribute \\\'name\\\'",)\',)',)'
      
 ## To-dos 
 
  - Finish K-Bucket implementation, including depth (shared_prefix) method 
  - Investigate routing table structure, including how buckets are splitted 
  
