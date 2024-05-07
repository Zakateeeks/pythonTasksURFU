# Befunge interpreter #

## Usage: ##

```
python interpreter.py <filename.bf> 
```

## Quick reference ##

 Character            | Description                                                                       
 ----------------------|----------------------------------------------------------------------------------- 
 `0-9`                | Push this number to the stack                                                     
 `+`                  | Pop `a` and `b`, then push `a+b`.                                                
 `-`                  | Pop `a` and `b`, then push `a-b`.                                                 
 `*`                  | Pop `a` and `b`, then push `a*b`.                                                 
 `/`                  | Pop `a` and `b`, then push `floor(b/a)`, provided that `a` is not zero.           
 `%`                  | Pop `a` and `b`, then push `a (mod b)`.                                           
 `!`                  | Pop `a`. If `a = 0`, push 1, otherwise push 0.                                    
 `'`                | Pop `a` and `b`, then push 1 if `b > a`, otherwise 0.                             
 `>`                  | Move right.                                                                       
 `<`                  | Move left.                                                                        
 `^`                  | Move up.                                                                         
 `v`                  | Move down.                                                                        
 `?`                  | Move in a random direction.                                                       
 `_`                  | Pop `a`. If `a = 0`, move right, otherwise move left.                             
 <code>&#124;</code> | Pop `a`. If `a = 0` , move down, otherwise move up.                               
 `"`                  | Start string mode. Push each characters ASCII value all the way up to the next ". 
 `:`                  | Duplicate value on top of the stack.                                             
 `\ `                 | Swap the two values on top of the stack.                                         
 `$`                  | Remove the value on top of the stack.                                             
 `.`                  | Pop `a`. Output the integer value of `a`.                                         
 `,`                  | Pop `a`. Output `chr(a)`.                                                         
 `#`                  | Skip next cell.                                                                   
 `p`                  | Pop `y`, `y` and `v`. Change the character in position `(x,y)` to `chr(v)`.       
 `g`                  | Pop `y` and `x` , the push the ASCII value of the character in position `(x,y)`.  
 `&`                  | Prompt user for a number and push it.                                             
 `~`               | Prompt user for a character and push its ASCII value.                             
 `@`                  | Stop instruction pointer                                                          

