import tensorflow as tf
import numpy as np
import random

# 批处理
BATCH_SIZE = 32
# 词向量维度
EMBEDDING_SIZE = 128
# 上下文窗口大小
WINDOW_SIZE = 4

VALID_SIZE = 16

VALID_WINDOW = 100

VALID_EXAMPLES = np.array(random.sample(range(VALID_WINDOW), VALID_SIZE))
VALID_EXAMPLES = np.append(VALID_EXAMPLES, random.sample(range(1000, 1000+VALID_WINDOW), VALID_SIZE), axis=0)
# 样本数量
NUM_SAMPLES = 32

# 根据占位符定义输入和输出
train_datasets = tf.placeholder(dtype=tf.int32, shape=[BATCH_SIZE])
train_labels = tf.placeholder(dtype=tf.int32, shape=[BATCH_SIZE, 1])
valid_datasets = tf.constant(VALID_EXAMPLES, dtype=tf.int32)

session = tf.Session()
session.run()