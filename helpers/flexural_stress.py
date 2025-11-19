def Rect_I(centroid, h, b, local_centroids):
    I=0
    for i in range(len(h)):
        I+=b[i]*(h[i]**3)/12 + (b[i]*h[i])*((local_centroids[i]-centroid)**2)
    return I

def Design2_centroid(w,h):
    return (2*1.27*h*(h/2)+(h-0.635)*1.27*5*2+(h+1.27)*2*1.27*w)/(2*1.27*h+2*1.27*5+2*1.27*w)

def Design2_I(w,h):
    centroid=Design2_centroid(w,h)
    height=[h,h,1.27,1.27,2*1.27]
    b=[1.27,1.27,5,5,w]
    local_centroids=[h/2,h/2,h-0.635,h-0.635,h+1.27]
    return Rect_I(centroid,height,b,local_centroids)

def flexural_tens(I,centroid,M_max=85910):
    flex_tens_stress=(M_max*centroid/I)
    print("Flexural Tensile Stress: " + str(flex_tens_stress))
    FOS=30/flex_tens_stress
    print("FOS(Flexural Tension) = "+str(FOS))

def flexural_comp(I,centroid, y_max, M_max=85910):
    flex_comp_stress=(M_max*(y_max-centroid))/I
    print("Flexural Compressive Stress: " + str(flex_comp_stress))
    FOS=6/flex_comp_stress
    print("FOS(Flexural Compression) = "+str(FOS))

def Design2_Q_centroid(w,h):
    centroid = Design2_centroid(w, h)
    if centroid>h-1.27:
        print("Double check centroidal axis! This function will not apply here")
    else:
        Q=centroid*1.27*2*(centroid/2)
        return Q

def Design2_Q_glue_top(w,h):
    centroid = Design2_centroid(w, h)
    Q=1.27*w*(h+1.27+0.635-centroid)
    return Q

def Design2_Q_glue_middle(w,h):
    centroid = Design2_centroid(w, h)
    Q=2*1.27*w*(h+1.27+1.27-centroid)
    return Q

def shear(Q,I,b):
    shear_stress = (-323 * Q) / (I*b)
    print("Shear Stress (matboard): " + str(shear_stress))
    FOS = 4 / shear_stress
    print("FOS(Shear (matboard)) = " + str(FOS))

def glue_shear(Q,I,b):
    shear_stress = (-323 * Q) / (I*b)
    print("Shear Stress (glue): " + str(shear_stress))
    FOS = 2 / shear_stress
    print("FOS(Shear (glue)) = " + str(FOS))

if __name__=="__main__":
    # print(Rect_I(55.8, [78.73,78.73,1.27,1.27,1.27],[1.27,1.27,5,5,100],[39.4,39.4,78.1,78.1,79.4]))
    # print(Design2_centroid(100,77.46))
    # print(Design2_I(100,77.46))
    # flexural_tens(279000,61.7)
    # flexural_comp(279000,61.7,80)
    # shear(Design2_Q_centroid(100,77.46),279000, 2.54)
    # glue_shear(Design2_Q_glue_top(100,77.46),279000, 100)
    # glue_shear(Design2_Q_glue_middle(100,77.46),279000, 10)
    print(flexural_comp(2105000,150.23,200))
    print(flexural_tens(2105000,150.23))
