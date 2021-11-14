import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
import os
from PIL import Image
import numpy as np
import cv2

from tensorflow.examples.tutorials.mnist import input_data

mnist = input_data.read_data_sets('./MNIST',one_hot=True)

batch_size = 300

def add_layer(input_data,input_num,output_num,activation_function=None):
    #output=input_data*weight+bias
    w = tf.Variable(initial_value=tf.random_normal(shape=[input_num,output_num]))
    b = tf.Variable(initial_value=tf.random_normal(shape=[1,output_num]))
    output = tf.add(tf.matmul(input_data,w),b)
    
    #activation? output = activation_function(output): output
    if activation_function:
        output = activation_function(output)
    return output

def build_nn(data):
    hidden_layer1 = add_layer(data,784,100,activation_function=tf.nn.sigmoid)
    hidden_layer2 = add_layer(hidden_layer1,100,50,activation_function=tf.nn.sigmoid)
    output_layer = add_layer(hidden_layer2,50,10)
    return output_layer

def read_data(path):
    image = cv2.imread(path,cv2.IMREAD_GRAYSCALE)
    # 1.square??? ========> square
    # 2.gray ok
    # 3.28*28
    processed_image = cv2.resize(image,dsize=(28,28))
    processed_image = np.resize(processed_image,new_shape=(1,784))
    return image,processed_image
    

def train_nn():
    mg = tf.Graph()
    with mg.as_default():
        x = tf.placeholder(dtype=tf.float32,shape=[None,784],name='x')
        #label
        y = tf.placeholder(dtype=tf.float32,shape=[None,10],name='y')
        
        output = build_nn(x)

        loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y,logits=output))
        optimizer = tf.train.GradientDescentOptimizer(learning_rate=1).minimize(loss)

        saver = tf.train.Saver()

        with tf.Session(graph = mg) as sess:
            sess.run(tf.global_variables_initializer())
            if not os.path.exists('./Mnist_model/checkpoint'):
                for i in range(300):
                    epoch_cost = 0
                    for _ in range(int(mnist.train.num_examples / batch_size)):
                        x_data,y_data = mnist.train.next_batch(batch_size)
                        cost,_ = sess.run([loss,optimizer],feed_dict={x:x_data,y:y_data})
                        epoch_cost += cost
                    print('Epoch',i,': ',epoch_cost)
                accuracy = tf.reduce_mean(tf.cast(tf.equal(tf.argmax(y,1),tf.argmax(output,1)),tf.float32))
                acc = sess.run(accuracy,feed_dict={x:mnist.test.images,y:mnist.test.labels})
                print(acc)
                saver.save(sess, './Mnist_model/mnist.ckpt')
            else:
                saver.restore(sess, './Mnist_model/mnist.ckpt')
                image_path = './only.png'
                image,processed_image = read_data(image_path)
                result = sess.run(output,feed_dict={x:processed_image})
                result = np.argmax(result,1)
                return result
def main():
    if os.path.exists('./Mnist_model/checkpoint'):
        result = train_nn()
        return result
    elif not os.path.exists('./Mnist_model/checkpoint'):
        train_nn()
