# .. This code is for the design of Hilbert resonators ..
# .. Conversions mm to Pixel  pixel = (DPI/25.4) 
# .. Import the library ..
import PIL
from PIL import Image
import ezdxf
from ezdxf import units
from turtle import *
# .. Define the Functions ..
def hilbert(level, angle, step):
    if level == 0:
        return
#
    right(angle)
    hilbert(level - 1, -angle, step)
    forward(step)
    left(angle)
    hilbert(level - 1, angle, step)
    forward(step)
    hilbert(level - 1, angle, step)
    left(angle)
    forward(step)
    hilbert(level - 1, -angle, step)
    right(angle)
# .. This routine will save the images ..
def save_image(NomeFile):
    canvas = getscreen().getcanvas()
    canvas.postscript(file=NomeFile)
# .. Estimates the length of the Hilbert curvo of level n ..
def curve_length_freq(side_square,level,EPS):
    C0 = 299792458 # .. Light velocity ..
    length = side_square*(2**level - 1/(2**level))
    # .. Estimated resonance frequency
    frequency = C0/(2*length*1e-3)*pow(EPS,1/2)
    return length,frequency
# .. Calculate the length of the curve with a fixed side to obtain the correct resonance ..
def resonator_synthesis_fixed_side(frequency,EPS,side_square):
    MHz = 1e6
    mm = 1e3
    C0 = 299792458
    length = C0/((2*frequency*1e6)*pow(EPS,1/2))
    print("Desired length:",length)
    print("Desired side square:",side_square)
    estimated_length = []
    for I_X_FOR in range(10):
        estimated_length.append(abs(side_square*1e-3*(2**I_X_FOR - 1/(2**I_X_FOR))-(length)))  
        print("Estimated length:",estimated_length[I_X_FOR],"level:",I_X_FOR)  
    min_value = min(estimated_length)
    level = estimated_length.index(min_value)
    print("Minimum Error:",min_value,"Index:",level)
    return level
# .. Calculate the side of the square to obtain the correct resonance ..
def resonator_synthesis(frequency,EPS,level):
    MHz = 1e6
    mm = 1e3
    C0 = 299792458
    length = C0/((2*frequency*1e6)*pow(EPS,1/2))
    print("lunghezza:",length)
    side_square = length/(2**level - 1/(2**level))
    print("side square:",side_square)
    return side_square*mm
# .. Convert the length from mm into pixel considerind the DPI ..
def mm_2_pixel(DPI,length_mm):
    pixel = length_mm*(DPI/25.4)
    return int(pixel)
# .. This Function shows the Hilbert curve with Turtle ..
def turtle_visualization(level_dpi,frequency,square_side,level,angle,trace_thickness,EPS,filename):
    Hilbert_length, Estimated_Freq =curve_length_freq(square_side,level,EPS)
    Estimated_Freq = round(Estimated_Freq/1e6)
    trace_size =  mm_2_pixel(level_dpi,trace_thickness)
    canvas_size = mm_2_pixel(level_dpi,square_side)/2
    penup()
    goto(-canvas_size, canvas_size)
    canvas_low_x = -256
    canvas_high_y = 256
    goto(canvas_low_x, canvas_high_y)
    style = ('Courier',20, 'bold')
    write("Desired Frequ.:"+ str(frequency) +"[MHz]", font=style)
    goto(canvas_low_x, canvas_high_y-20)
    write("Length:"+ str(round(Hilbert_length)) +"[mm]" + "     Estimated Freq.:"+ str(Estimated_Freq)+" [MHz]", font=style)
    goto(canvas_low_x, canvas_high_y-40)
    dummy_string= "Side: " + str(round(square_side)) + "[mm] " + "Line Width: " + str(trace_thickness) + "[mm]"
    write(dummy_string, font=style)
    goto(canvas_low_x, canvas_high_y-60)
    write('Level:'+str(level), font=style)
   # 
    hideturtle()
    speed("fastest")  
    #speed("slowest")  
    pensize(trace_size)
    penup()
    goto(-canvas_size / 2.0, canvas_size / 2.0)
    pendown()
    hilbert(level, angle, canvas_size/(2**level-1))
    save_image(filename+".ps")
    done()
# .. The following function are used to create a DXF file .. 
# .. This function 
def hilbert_iterative(iterations):
    # .. L-System re-writing rules ..
    rules = {
        'A': '+BF-AFA-FB+',
        'B': '-AF+BFB+FA-'
    } 
    # .. Begin of the curve ..
    current_string = 'A'
    # .. Itertive L-System string generation ..
    for _ in range(iterations):
        next_string = []
        for char in current_string:
            next_string.append(rules.get(char, char))
        current_string = "".join(next_string)
    # .. Return the curve description using L-system method ..  
    return current_string
# .. This subroutine accept the PCB trace thickness in mm and return the ezdxf format ..
def DXF_Thickness_Conversion(thickness):
    if(thickness<0.13 or thickness == 0.13):
        return int(13)
    elif((thickness>0.13) and (thickness<=0.15)):
        return int(15)
    elif((thickness>0.15) and (thickness<=0.20)):
        return int(20)
    elif((thickness>0.20) and (thickness<=0.25)):
        return int(25)
    elif((thickness>0.25) and (thickness<=0.30)):
        return int(30)
    elif((thickness>0.3) and (thickness<=0.40)):
        return int(40)
    elif((thickness>0.4) and (thickness<=0.50)):
        return int(50)
    elif((thickness>0.5) and (thickness<=0.70)):
        return int(70)
    elif((thickness>0.7) and (thickness<=1.0)):
        return int(100)
    elif((thickness>1.0) and (thickness<=2.0) or (thickness>2.0)):
        return int(200)
# .. This function generates a DXF file for PCB printing ..
def draw_hilbert_dxf(L_STRING, step, angle, TRACE_THICKNESS, FILE_NAME):
    # .. Convert the trace thickness in DXF format ..
    TRACE_DXF = DXF_Thickness_Conversion(TRACE_THICKNESS)
    # .. Create a new DXF document ..
    doc = ezdxf.new("R2010", setup=True)
    # .. Set the model units in mm ..
    doc.header['$INSUNITS'] = units.MM
    # .. Set the line thickness visible ..
    doc.header['$LWDISPLAY'] = 1
    # .. Defines the model spaces .. 
    msp = doc.modelspace()
    #
    START_X = 0
    START_Y = 0
    ANGLE=0
    INDEX=0
    # .. Movements esecutions ..
    for char in L_STRING:
        if char == 'F':      
            if(ANGLE>360):
                ANGLE_R = ANGLE - (ANGLE // 360)*360  
                ANGLE=ANGLE_R
            elif(ANGLE<-360):    
                ANGLE_R = ANGLE + (-ANGLE // 360)*360
                ANGLE=ANGLE_R
            INDEX+=1
            if(ANGLE==0 or ANGLE==360 or ANGLE==-360):
                msp.add_line((START_X, START_Y),(START_X+step, START_Y), dxfattribs={"lineweight":TRACE_DXF})
                START_X=START_X+step
                INDEX+=1
            elif(ANGLE==90 or ANGLE==-270):
                msp.add_line((START_X, START_Y),(START_X, START_Y+step), dxfattribs={"lineweight":TRACE_DXF})
                START_Y=START_Y+step
                INDEX+=1
            elif(ANGLE==-90 or ANGLE==270):
                msp.add_line((START_X, START_Y),(START_X, START_Y-step), dxfattribs={"lineweight":TRACE_DXF})
                START_Y=START_Y-step
                INDEX+=1
            elif(ANGLE==180 or ANGLE==-180):
                msp.add_line((START_X, START_Y),(START_X-step, START_Y), dxfattribs={"lineweight":TRACE_DXF})
                START_X=START_X-step
                INDEX+=1
        elif char == '+':
            ANGLE+=angle
        elif char == '-':
            ANGLE-=angle         
        # .. Save file ..      
        doc.saveas(FILE_NAME)            
    print("The DXF has been created") 
# .. Main function ..
def main():
    angle = 90 # .. Fixed to 90 because it define the standard Hilbert curve ..
    level_dpi = int(input("Insert the DPI:"))
    print(level_dpi)
    frequency = float(input("Insert the frequency [MHz]:"))
    print(frequency)
    # .. Define the line thickness for DXF standard ..
    # .. [13 15 20 25 30 40 50 70 100 200]= [0.13 0.15 0.20 0.25 0.3 0.4 0.5 0.7 1.0 2.0] mm
    trace_thickness = float(input("Insert the trace thickness [mm]:"))
    print(trace_thickness)
    EPS = float(input("Insert substrate EPS:"))
    print(EPS)
    FLAG_MODE = int(input("Insert mode 0 fixed side, 1 fixed level, 2 fixed side and level:"))
    print(FLAG_MODE)
    if(FLAG_MODE == 0):
        square_side = float(input("Insert the square side [mm]:"))
        print(square_side)
        level = resonator_synthesis_fixed_side(frequency,EPS,square_side)
    elif(FLAG_MODE == 1):
        level = int(input("Insert the level:"))
        print(level)
        square_side = resonator_synthesis(frequency,EPS,level)
    elif(FLAG_MODE == 2):
        square_side = float(input("Insert the square side [mm]:"))
        print(square_side)
        level = int(input("Insert the level:"))
        print(level)
    #
    file_name = input("Insert the Filename:") 
    print(file_name)
    # .. Visualize the Hilbert Curve with the turtle tool ..
    turtle_visualization(level_dpi,frequency,square_side,level,angle, trace_thickness,EPS,file_name)
    # .. Creation of DXF file ..
    HILBERT_STR = hilbert_iterative(level)
    draw_hilbert_dxf(HILBERT_STR,square_side, angle, trace_thickness,file_name+'.dxf')
 
if __name__ == '__main__':
    main()