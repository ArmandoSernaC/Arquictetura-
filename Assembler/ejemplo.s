## DESIGN PROBLEM M02: Multiply two matrixes [nxn] * [nx1] = [nx1]

############################################
#### Data memory
############################################
.data 

a: .word 0x00000004 #4 dec Aqui guardamos el numero 4 en el primer espacio de memoria disponible
b: .word 0x00000002 #2 dec Aqui guardamos el numero 4 en el primer espacio de memoria disponible

res: .word 0x10000100 #Memory address Declaramos la direccion de memoria de donde se va a almacenar la respuesta



############################################
#### Instruction memory
############################################
.text

#### Guide to the correct use of processor registers:
## x0 = hardwired to zero
## x1 = return address by caller
## x2 = stack pointer by caller and callee
## x3 = global data pointer
## x4 = thread pointer
## x5,x6,x7,x28,x29,x30,x31 = used by caller
## x8,x9,x18-x27 = used by calle
## x10 - x17 = return/arguments spaces by caller and callee
    
main: ## caller main function
    # your code here!!
    
    lw x5, 0(x3) # load a
    lw x6, 4(x3) #load b 
    lw x31, 8(x3) # load res 
    
    #Pasamos las variables de los registros del caller a los registros
    #que va utilizar el callee 
    add x11,x5,x0  #x11=x5=a
    add x12,x6,x0  #x11=x6=b  
    
    
    jal x1,sum  #Saltamos a la instruccion suma 
    
    add x28, x10,x0 #x28=x10=a+b
    
    add x11,x28 x0 #Pasar los registros que va a usar div
    
    add x29,x10,x0 #x29 =(a+b)/2 
    
    sw x29, 0(x31) #Se guarda la respuesta en la direccion de memoria establecida anteriormente

    beq x0,x0,end #Se termina el programa
sum: #Callee  x10=x11+x12
    add x10, x11,x12
    jalr x8,x1,0 #Saltamos de regreso al main 

div: #Calle x10=x11/2
    srai x10,x11,1
    jal x1, div
    jalr x8,x1,0
    
    


end:nop