'''*****************************************************************************
   Just as the content of ppt, the program is in order to encode a message in
   an image, then decode the image with the secret message.
   
   There are three parts about the program--code_message(), decode_message()
   and size_message().
   The code_message() includes read_image_file(), read_message_file(),
   add_text_bits() and save_image_file().
   The decode_message() includes extract_text_bits(), assemble_text_bits() and
   save_message_file()
   Function of each function will be explained below.
   *****************************************************************************
   
   *****************************************************************************
'''



'''*****************************************************************************
   read a .bmp file with the way of bytes using 'rb' and then put the data into
   a bytearray return the bytearray
   *****************************************************************************
'''
def read_image_file(filename):
    file = open(filename, 'rb')
    msg = bytearray(file.read())
    file.close()
    return msg



'''*****************************************************************************
   read a .txt file and make the every character into ASC code
   the purpose is getting the every single bit and add it into a list
   the list will be employed in the next function so I need to return it
   *****************************************************************************
'''
def read_message_file(filename):
    file = open(filename, 'r')     #just open as 'r' the data is character
    text = file.read()
    L = []
    for letter in text:        
        w = ord(letter)         #get the character's ASC code value
        #print(w)
        L.append(w & 0b00000001)   #from the lowest position to the highest
        for x in range(0,7):       #position(maybe some zeroes) put the bit
            w = w >> 1             #into a list
            L.append( w & 0b00000001)
    #print(L)
    file.close()
    return L



'''*****************************************************************************
   use the list of read_message_file, this is what we want to save in the image
   msg is the byte of image, now the start position is 53+p and if x in the list
   is 0 we operate it with 0b11111110 using &, and if it is 1 operate is with
   0b00000001 using |, through the loop we can keep every bit in the image
   finally we should return the list which saved changed bytes in the image
   *****************************************************************************
'''
def add_text_bits(msg, L, p, q):
    L2 = []
    pos = 53 + p        #Because the list starts at zero the, so number 53 is 
    for x in L:         #the 54th element
        w = msg[pos]
        if x == 0:
            w = w & 0b11111110  
        else:
            w = w | 0b00000001
        L2.append(w)
        pos += q
    return L2




'''*****************************************************************************
   The last step of the part code_message is saving the new image bytes.
   The variable index is the position in the list which saves the changed bytes.
   When the changed bytes have been written into new file the index must add 1.
   If the variable x equates the varibale pos, the written byte should be the
   changed byte, otherwise the byte is the initial byte.
   *****************************************************************************
'''
def save_image_file(filename, p, q, msg,L2):
    tf = open(filename, 'wb')
    pos = 53 + p
    index = 0        #the variable is like a position pointer 
    for x in range(0, len(msg)):  #if the position is 53+p or 53+p+q or ...
        if x == pos and index < len(L2): #the changed bytes need to be written
            #but if the element has been all written, the it can't go into
            #the if sentence
            tf.write(L2[index].to_bytes(1,byteorder = 'big'))
            pos += q
            index += 1
        else:
            tf.write(msg[x].to_bytes(1, byteorder = 'big'))
    tf.close()




'''*****************************************************************************
   This function is the integration of above functions.
   We just need to call above functions and give them correct parameters.
   *****************************************************************************
'''
def code_message(bmp_infile, bmp_outfile, message_file, p, q):
     msg = read_image_file(bmp_infile)
     L = read_message_file(message_file)
     L2 = add_text_bits(msg, L, p, q)
     save_image_file(bmp_outfile, p, q, msg, L2)
     print('Encrypt successfully')




'''*****************************************************************************
   The fllowing functions are the second part.
   *****************************************************************************
'''




'''*****************************************************************************
   Just as the name of the function, it extracts changed bytes in the new image.
   But first we need to know the number of bit, it's value is in variable size.
   We can use os module to achieve it. In order to get every single bit, I make
   the bytes in correct position of the new image file operate with 0b00000001
   and save it in a list.
   *****************************************************************************
'''
import os
def extract_text_bits(filename, msg, p, q):
    size = os.path.getsize(filename)*8 #the number of bits we encrypt
    list1 = []
    pos = 53 + p
    for x in range(0, size):
        w = msg[pos] & 0b00000001  #get the last bit which is encrypted before
        list1.append(w)
        pos += q
    #print(len(list1))
    #print(size)
    return list1




'''*****************************************************************************
   We all know a byte is 8 bits, so I need to synthesize every eight bit binary
   array into a byte and through chr() turn it into a character. It will be
   saved in a list, at last, return the list
   *****************************************************************************
'''
def assemble_text_bits(list1):
    list2 = []
    length = len(list1)   #the number of all bits
    for x in range(0, length, 8):  #interval is 8
        bits = list1[x: x+8]       #get 8 bits once 
        #print(bits)
        c = 0b0
        for i in range(7, -1, -1):  #becaues when we save them in the list is
            c = c | bits[i]         #in order from low to high 
            if i != 0:   #it will left shift 7 digit rather than 8 digit
                c = c << 1
        list2.append(chr(c))  #the final answei is character not byte so
        #print(chr(c))        #we need chr()
    return list2




'''*****************************************************************************
   After I get the secret message as character, I just need to write it in
   a file in the way of 'w'.
   *****************************************************************************
'''
def save_message_file(filename, list2):
    tf = open(filename, 'w')
    for x in list2:
        tf.write(x)
    tf.close()




'''*****************************************************************************
   In the function, I call above functions and give appropriate parameters
   *****************************************************************************
'''
def decode_message(bmp_outfile, message_file, message_outfile, p, q):
    msg = read_image_file(bmp_outfile)  #the parameter must be the new .bmp
    list1 = extract_text_bits(message_file, msg, p, q)
    list2 = assemble_text_bits(list1)
    save_message_file(message_outfile, list2)
    print('Decrypt successfully')







'''*****************************************************************************
   The third part is a function which can whether the message can be encrypted
   successfully or not.
   If the message file's bytes multiply 8 exceeds a certain number, the
   encryption will not be successful. The premise is that the correct
   parameters are given.
   *****************************************************************************
'''
def size_message(bmp_infile, message_file, p, q):
    size_in_bytes = os.path.getsize(bmp_infile)
    size_in_bits = os.path.getsize(message_file)*8
    num = (size_in_bytes -(53 + p))/q + 1   #the capacity of a .bmp file when 
    if num > size_in_bits:                  #it's used to encrypt message
        return True
    else:
        return False



#The following code can appear in the cmd or console, but I think put it
#at the end of the program is also convenient.
if size_message('flowers.bmp','text.txt',1 ,2):
    code_message('flowers.bmp', 'tf.bmp', 'text.txt', 1, 2)
    decode_message('tf.bmp', 'text.txt', 'tf.txt', 1, 2)

else:
    print('The message is too long!')


'''the output is:
Encrypt successfully
Decrypt successfully
>>>
the tf.txt content is the same with text.txt and
the two .bmp file look like the same one



if the message is too long the output is:
The message is too long!
>>>
thre is not a tf.txt and tf.bmp
'''








        
