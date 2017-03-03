import socket
import time

#PS3 DS3 Controller Maps - axis indexes
#{0, 255} means a value of update(or 255
#[-128, 127] means a value in the -128 to 127 range 
LEFT_STICK_X =0 #LEFT stick x [-128, 127] 
LEFT_STICK_Y =1 #LEFT stick y [-128, 127] 
RIGHT_STICK_X =2 #RIGHT stick x [-128, 127] 
RIGHT_STICK_Y =3 #RIGHT stick y [-128, 127] 
ACC_X =4 #acc x [-512, 511] 
ACC_Y =5 #acc y [-512, 511] 	
ACC_Z =6 #acc z [-512, 511]
GYRO =7 #gyro [-512, 511] 
SELECT =8 #select {0, 255}
START =9 #start {0, 255} 
PS =10 #ps {0, 255}
UP =11 #up [0, 255] 
RIGHT =12 #RIGHT [0, 255] 
DOWN =13 #down [0, 255] 
LEFT =14 #LEFT [0, 255]
TRIANGLE =15 #triangle [0, 255] 
CIRCLE =16 #circle [0, 255] 
CROSS =17 #CROSS [0, 255]
SQUARE =18 #square [0, 255]
L1 =19 #l1 [0, 255] 
R1 =20 #e1 [0, 255] 
L2 =21 #l2 [0, 255] 
R2 =22 #r2 [0, 255] 
L3 =23 #l3 [0, 255] 
R3 =24 #r3 [0, 255] 
    
codeToString = ["LEFT_STICK_X","LEFT_STICK_Y","RIGHT_STICK_X","RIGHT_STICK_Y","ACC_X","ACC_Y","ACC_Z","GYRO","SELECT","START","PS","UP","RIGHT","DOWN","LEFT","TRIANGLE","CIRCLE","CROSS","SQUARE","L1","R1","L2","R2","L3","R3"]

'''
KeyASCII      ASCII   Common Name
K_BACKSPACE   \b      backspace
K_TAB         \t      tab
K_CLEAR               clear
K_RETURN      \r      return
K_PAUSE               pause
K_ESCAPE      ^[      escape
K_SPACE               space
K_EXCLAIM     !       exclaim
K_QUOTEDBL    "       quotedbl
K_HASH        #       hash
K_DOLLAR      $       dollar
K_AMPERSAND   &       ampersand
K_QUOTE               quote
K_LEFTPAREN   (       LEFT parenthesis
K_RIGHTPAREN  )       RIGHT parenthesis
K_ASTERISK    *       asterisk
K_PLUS        +       plus sign
K_COMMA       ,       comma
K_MINUS       -       minus sign
K_PERIOD      .       period
K_SLASH       /       forward slash
K_update(          update(      0
K_1           1       1
K_2           2       2
K_3           3       3
K_4           4       4
K_5           5       5
K_6           6       6
K_7           7       7
K_8           8       8
K_9           9       9
K_COLON       :       colon
K_SEMICOLON   ;       semicolon
K_LESS        <       less-than sign
K_EQUALS      =       equals sign
K_GREATER     >       greater-than sign
K_QUESTION    ?       question mark
K_AT          @       at
K_LEFTBRACKET [       LEFT bracket
K_BACKSLASH   \       backslash
K_RIGHTBRACKET ]      RIGHT bracket
K_CARET       ^       caret
K_UNDERSCORE  _       underscore
K_BACKQUOTE   `       grave
K_a           a       a
K_b           b       b
K_c           c       c
K_d           d       d
K_e           e       e
K_f           f       f
K_g           g       g
K_h           h       h
K_i           i       i
K_j           j       j
K_k           k       k
K_l           l       l
K_m           m       m
K_n           n       n
K_o           o       o
K_p           p       p
K_q           q       q
K_r           r       r
K_s           s       s
K_t           t       t
K_u           u       u
K_v           v       v
K_w           w       w
K_x           x       x
K_y           y       y
K_z           z       z
K_DELETE              delete
K_KPupdate(                keypad 0
K_KP1                 keypad 1
K_KP2                 keypad 2
K_KP3                 keypad 3
K_KP4                 keypad 4
K_KP5                 keypad 5
K_KP6                 keypad 6
K_KP7                 keypad 7
K_KP8                 keypad 8
K_KP9                 keypad 9
K_KP_PERIOD   .       keypad period
K_KP_DIVIDE   /       keypad divide
K_KP_MULTIPLY *       keypad multiply
K_KP_MINUS    -       keypad minus
K_KP_PLUS     +       keypad plus
K_KP_ENTER    \r      keypad enter
K_KP_EQUALS   =       keypad equals
K_UP                  up arrow
K_DOWN                down arrow
K_RIGHT               RIGHT arrow
K_LEFT                LEFT arrow
K_INSERT              insert
K_HOME                home
K_END                 end
K_PAGEUP              page up
K_PAGEDOWN            page down
K_F1                  F1
K_F2                  F2
K_F3                  F3
K_F4                  F4
K_F5                  F5
K_F6                  F6
K_F7                  F7
K_F8                  F8
K_F9                  F9
K_F1update(                F10
K_F11                 F11
K_F12                 F12
K_F13                 F13
K_F14                 F14
K_F15                 F15
K_NUMLOCK             numlock
K_CAPSLOCK            capslock
K_SCROLLOCK           scrollock
K_RSHIFT              RIGHT shift
K_LSHIFT              LEFT shift
K_RCTRL               RIGHT ctrl
K_LCTRL               LEFT ctrl
K_RALT                RIGHT alt
K_LALT                LEFT alt
K_RMETA               RIGHT meta
K_LMETA               LEFT meta
K_LSUPER              LEFT windows key
K_RSUPER              RIGHT windows key
K_MODE                mode shift
K_HELP                help
K_PRINT               print screen
K_SYSREQ              sysrq
K_BREAK               break
K_MENU                menu
K_POWER               power
K_EURO                euro

The keyboard also has a list of modifier states that can be assembled bit bitwise ORing them together.

KMOD_NONE, KMOD_LSHIFT, KMOD_RSHIFT, KMOD_SHIFT, KMOD_CAPS,
KMOD_LCTRL, KMOD_RCTRL, KMOD_CTRL, KMOD_LALT, KMOD_RALT,
KMOD_ALT, KMOD_LMETA, KMOD_RMETA, KMOD_META, KMOD_NUM, KMOD_MODE
'''

UDP_IP = "127.0.0.1"
UDP_PORT = 51914

print ("UDP target IP:", UDP_IP)
print ("UDP target port:", UDP_PORT)

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

# byte array conversion methods

def intToBytes(n,b,offset):
    #b = bytearray([0, 0, 0, 0])   # init
    b[offset+0] = n & 0xFF
    n >>= 8
    b[offset+1] = n & 0xFF
    n >>= 8
    b[offset+2] = n & 0xFF
    n >>= 8
    b[offset+3] = n & 0xFF    
    
    # Return the result or as bytearray or as bytes (commented out)
    ##return bytes(b)  # uncomment if you need
    #return b
    
    
def bytesToInt(b, offset):
    n = (b[offset+3]<<24) + (b[offset+2]<<16) + (b[offset+1]<<8) + b[offset+0]
    return n

def sendRecv(message):
    global sock,UDP_IP,UDP_PORT
    sock.sendto(message, (UDP_IP, UDP_PORT))
    #while True:
    data, addr = sock.recvfrom(4192) # buffer size is 1024 bytes
    #print ("received message:", data)
    return data

def send(message):
    global sock,UDP_IP,UDP_PORT
    #print("send message")
    sock.sendto(message, (UDP_IP, UDP_PORT))

def update(delayVal,cmd,value):
    global prevTime, prevCmd
    time.sleep(delayVal)#-prevTime)
    #print ("executeAt: ",executeAt)
    #print ("sleep: ",executeAt-prevTime)
    #print ("cmd: ",cmd)
    #print ("value: ",value)
    print("update("+str(delayVal)+", "+codeToString[cmd]+", "+str(value)+")")
    #prevTime = delayVal
    prevCmd = cmd
    do_update(cmd,value)

def do_update(KEY,value):
    global MESSAGE
    if bytesToInt(MESSAGE, 2+KEY*4) != value:
        intToBytes(value,MESSAGE,2+KEY*4)
        send(MESSAGE)

#basic message, all axis off
MESSAGE = bytearray(157)
MESSAGE[0]=0xff
MESSAGE[1]=0x9c

#key=None

prevTime=0
prevCmd = None



def quitGT5():
    update(2.452928304672241, PS, 255)
    update(0.16549062728881836, PS, 0)
    update(3.772346258163452, CROSS, 255)
    update(0.13194537162780762, CROSS, 0)
    update(2.811427593231201, LEFT, 255)
    update(0.13286161422729492, LEFT, 0)
    update(4.364124298095703, CROSS, 255)
    update(0.13109803199768066, CROSS, 0)

def setController():
    update(0.0, LEFT, 255)
    update(0.19776463508605957, LEFT, 0)
    update(0.6940388679504395, LEFT, 255)
    update(0.19843125343322754, LEFT, 0)
    update(0.991696834564209, LEFT, 255)
    update(0.19772028923034668, LEFT, 0)
    update(0.7258071899414062, LEFT, 255)
    update(0.16529488563537598, LEFT, 0)
    update(1.0253369808197021, LEFT, 255)
    update(0.16504549980163574, LEFT, 0)
    update(2.2445030212402344, DOWN, 255)
    update(0.16490530967712402, DOWN, 0)
    update(0.6608078479766846, DOWN, 255)
    update(0.13375091552734375, DOWN, 0)
    update(0.23116397857666016, DOWN, 255)
    update(0.06551384925842285, DOWN, 0)
    update(0.13166069984436035, DOWN, 255)
    update(0.10067272186279297, DOWN, 0)
    update(1.090935468673706, DOWN, 255)
    update(0.09903836250305176, DOWN, 0)
    update(0.13172602653503418, DOWN, 255)
    update(0.0661017894744873, DOWN, 0)
    update(0.1317746639251709, DOWN, 255)
    update(0.03265881538391113, DOWN, 0)
    update(2.150562047958374, CROSS, 255)
    update(0.1315920352935791, CROSS, 0)
    update(1.8822617530822754, DOWN, 255)
    update(0.13321948051452637, DOWN, 0)
    update(0.7605011463165283, CROSS, 255)
    update(0.19968032836914062, CROSS, 0)
    update(0.8919796943664551, DOWN, 255)
    update(0.13195347785949707, DOWN, 0)
    update(0.8916900157928467, CROSS, 255)
    update(0.19755101203918457, CROSS, 0)
    update(4.129018783569336, CIRCLE, 255)
    update(0.13242006301879883, CIRCLE, 0)
    update(2.346317768096924, RIGHT, 255)
    update(0.16463565826416016, RIGHT, 0)
    update(0.1983795166015625, RIGHT, 255)
    update(0.16511964797973633, RIGHT, 0)
    update(0.26371335983276367, RIGHT, 255)
    update(0.13211727142333984, RIGHT, 0)
    update(0.16500616073608398, RIGHT, 255)
    update(0.09875869750976562, RIGHT, 0)
    update(1.3220233917236328, RIGHT, 255)
    update(0.19780826568603516, RIGHT, 0)
    update(1.4560623168945312, DOWN, 255)
    update(0.13224434852600098, DOWN, 0)

def startGT5(): #in Rome and drive a bit
    update(2.577549934387207, CROSS, 255)
    update(0.1651444435119629, CROSS, 0)
    update(53.28884744644165, CROSS, 255)
    update(0.1997969150543213, CROSS, 0)
    update(6.847616910934448, CROSS, 255)
    update(0.19855594635009766, CROSS, 0)
    update(8.620874404907227, CROSS, 255)
    update(0.1984109878540039, CROSS, 0)
    update(11.540334224700928, RIGHT, 255)
    update(0.19747257232666016, RIGHT, 0)
    update(1.7548072338104248, RIGHT, 255)
    update(0.20024895668029785, RIGHT, 0)
    update(0.9589612483978271, RIGHT, 255)
    update(0.2312326431274414, RIGHT, 0)
    update(2.017909288406372, DOWN, 255)
    update(0.16624021530151367, DOWN, 0)
    update(0.8258013725280762, CROSS, 255)
    update(0.19821763038635254, CROSS, 0)
    update(4.928144931793213, RIGHT, 255)
    update(0.16479873657226562, RIGHT, 0)
    update(0.2315692901611328, RIGHT, 255)
    update(0.16499686241149902, RIGHT, 0)
    update(0.1324293613433838, RIGHT, 255)
    update(0.1318824291229248, RIGHT, 0)
    update(1.8509235382080078, UP, 255)
    update(0.1315910816192627, UP, 0)
    update(1.2231659889221191, RIGHT, 255)
    update(0.16571998596191406, RIGHT, 0)
    update(0.19888758659362793, RIGHT, 255)
    update(0.16445255279541016, RIGHT, 0)
    update(0.16550397872924805, RIGHT, 255)
    update(0.131500244140625, RIGHT, 0)
    update(2.3152284622192383, LEFT, 255)
    update(0.16458606719970703, LEFT, 0)
    update(0.7932980060577393, CROSS, 255)
    update(0.16549897193908691, CROSS, 0)
    update(2.379965305328369, CROSS, 255)
    update(0.1318049430847168, CROSS, 0)
    update(1.917600393295288, CROSS, 255)
    update(0.1655874252319336, CROSS, 0)
    update(2.047126531600952, CROSS, 255)
    update(0.16536569595336914, CROSS, 0)
    update(17.725045680999756, R2, 255)
    update(0.16538763046264648, R2, 0)
    update(0.9587352275848389, CROSS, 255)
    update(0.2312939167022705, CROSS, 0)
    update(19.331735610961914, R2, 255)
    update(0.6598832607269287, R2, 0)
    update(0.3642079830169678, RIGHT, 255)
    update(0.5632283687591553, R2, 255)
    update(0.42987728118896484, R2, 0)
    update(0.3309745788574219, RIGHT, 0)
    update(0.7602870464324951, L2, 255)
    update(0.4300839900970459, LEFT, 255)
    update(1.3543753623962402, LEFT, 0)
    update(0.00010013580322265625, L2, 0)
    update(0.6279246807098389, R2, 255)
    update(3.8421778678894043, RIGHT, 255)
    update(0.36250758171081543, RIGHT, 0)
    update(0.4623842239379883, RIGHT, 255)
    update(0.16524910926818848, RIGHT, 0)
    update(0.39617109298706055, RIGHT, 255)
    update(0.6617152690887451, R2, 0)
    update(1.8487563133239746, RIGHT, 0)
    update(1.024705171585083, LEFT, 255)
    update(0.26456642150878906, LEFT, 0)
    update(0.16590237617492676, LEFT, 255)
    update(0.16479825973510742, LEFT, 0)
    update(0.36437463760375977, R2, 255)
    update(1.1560766696929932, LEFT, 255)
    update(0.5620150566101074, LEFT, 0)
    update(0.5606281757354736, RIGHT, 255)
    update(0.2644526958465576, RIGHT, 0)
    update(0.39609384536743164, RIGHT, 255)
    update(0.36315035820007324, RIGHT, 0)
    update(0.8579819202423096, LEFT, 255)
    update(0.2971010208129883, LEFT, 0)
    update(0.46346449851989746, LEFT, 255)
    update(0.19824457168579102, LEFT, 0)
    update(0.4614980220794678, LEFT, 255)
    update(0.33022022247314453, LEFT, 0)
    update(0.2649202346801758, LEFT, 255)
    update(0.06634831428527832, LEFT, 0)
    update(0.29760169982910156, LEFT, 255)
    update(0.09893679618835449, LEFT, 0)
    update(0.16470551490783691, R2, 0)

#setController()
#quitGT5()
#time.sleep(30)
startGT5()
quitGT5()
time.sleep(30)
startGT5()
quitGT5()