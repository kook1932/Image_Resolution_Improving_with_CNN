# -*- coding: utf-8 -*-
"""ModelTest_AWS.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ygtZ55bp3hy-E-I2mHDxrp61NW9wHdFQ
"""

import cv2, os, glob
import numpy as np
import matplotlib.pyplot as plt
from keras import backend as K
from keras.models import load_model
from keras.layers import Conv2D, Input, Activation
from keras.models import Model
from skimage.transform import pyramid_expand

class Subpixel(Conv2D):
    def __init__(self,
                 filters,
                 kernel_size,
                 r,
                 padding='valid',
                 data_format=None,
                 strides=(1,1),
                 activation=None,
                 use_bias=True,
                 kernel_initializer='glorot_uniform',
                 bias_initializer='zeros',
                 kernel_regularizer=None,
                 bias_regularizer=None,
                 activity_regularizer=None,
                 kernel_constraint=None,
                 bias_constraint=None,
                 **kwargs):
        super(Subpixel, self).__init__(
            filters=filters,
            kernel_size=kernel_size,
            strides=strides,
            padding=padding,
            data_format=data_format,
            activation=activation,
            use_bias=use_bias,
            kernel_initializer=kernel_initializer,
            bias_initializer=bias_initializer,
            kernel_regularizer=kernel_regularizer,
            bias_regularizer=bias_regularizer,
            activity_regularizer=activity_regularizer,
            kernel_constraint=kernel_constraint,
            bias_constraint=bias_constraint,
            **kwargs)
        self.r = r

    def _phase_shift(self, I):
        r = self.r
        bsize, a, b, c = I.get_shape().as_list()
        bsize = K.shape(I)[0] # Handling Dimension(None) type for undefined batch dim
        X = K.reshape(I, [bsize, a, b, int(c/(r*r)),r, r]) # bsize, a, b, c/(r*r), r, r
        X = K.permute_dimensions(X, (0, 1, 2, 5, 4, 3))  # bsize, a, b, r, r, c/(r*r)
        #Keras backend does not support tf.split, so in future versions this could be nicer
        X = [X[:,i,:,:,:,:] for i in range(a)] # a, [bsize, b, r, r, c/(r*r)
        X = K.concatenate(X, 2)  # bsize, b, a*r, r, c/(r*r)
        X = [X[:,i,:,:,:] for i in range(b)] # b, [bsize, r, r, c/(r*r)
        X = K.concatenate(X, 2)  # bsize, a*r, b*r, c/(r*r)
        return X

    def call(self, inputs):
        return self._phase_shift(super(Subpixel, self).call(inputs))

    def compute_output_shape(self, input_shape):
        unshifted = super(Subpixel, self).compute_output_shape(input_shape)
        return (unshifted[0], self.r*unshifted[1], self.r*unshifted[2], int(unshifted[3]/(self.r*self.r)))

    def get_config(self):
        config = super(Conv2D, self).get_config()
        #config.pop('rank')
        config.pop('dilation_rate')
        config['filters'] = int(config['filters'] / self.r*self.r)
        config['r'] = self.r
        return config

def modelProcessing(imageFileName):
    #모델 load
    model = load_model('/home/ec2-user/srservice/model/modeltest.h5',custom_objects={'Subpixel':Subpixel}) #aws 
    output_path = '/home/ec2-user/srservice/ResultOutput/' #aws 결과물이 저장될 경로

    #image load
    img=cv2.imread('/home/ec2-user/srservice/image/'+imageFileName)
    img_normalize=cv2.normalize(img.astype(np.float64), None, 0, 1, cv2.NORM_MINMAX)

    # 모델predict 동작 
    img_pred = model.predict(img_normalize.reshape((1, 200, 200, 3)))

    print(img_pred.shape)
    
    
    
    img_pred = np.clip(img_pred.reshape((800, 800, 3)), 0, 1)
    img_pred =(img_pred*255).astype(np.uint8)
  
    img_resize=cv2.resize(img_pred, dsize=(200,200), interpolation=cv2.INTER_AREA)

  # img_pred=cv2.cvtColor(img_pred, cv2.COLOR_BGR2RGB)
    

    #plt.axis('off') #세로,가로축 눈금표시 없에기
            
    #plt.xticks([]), plt.yticks([])#틱없에기
    #plt.tight_layout()
   
    
    #plt.imshow(img_pred)

    #plt.savefig(output_path+imageFileName)
    
    cv2.imwrite(output_path+imageFileName,img_resize)
