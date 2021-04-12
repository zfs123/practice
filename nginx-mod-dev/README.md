## Installation

   1. Configure Nginx adding this module with:
          
          Static Module : ./configure (...) --add-module=/path/to/nginx-hello-world-module
          Dynamic Module: ./configure (...) --add-dynamic-module=/path/to/nginx-hello-world-module
       
   2. Build Nginx as usual with `make`.
   
   3. Configure the module. The directive is `hello`
      that is supported in the **location** context only.
      
      Example:
          
          location = /test {
             
             hello on;
          
          }

      Now doing something like:
          
          curl -i http://example.com/test
          
      should return the **hello** string as the response body.
