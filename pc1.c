/*
问题描述：请用C语言编程，实现下述要求的程序。要求：
1.使用条件变量解决生产者、计算者、消费者问题；
2.系统中有3个线程：生产者、计算者、消费者，其中主线程作为生产者；
3.系统中有2个容量为4的缓冲区：buffer1、buffer2；
4.生产者生产'a'、'b'、'c'、‘d'、'e'、'f'、'g'、'h'八个字符，放入到buffer1；
5.计算者从buffer1取出字符，将小写字符转换为大写字符，放入到buffer2；
6.消费者从buffer2取出字符，将其打印到屏幕上。
*/
#include <stdio.h>
#include <unistd.h>
#include <pthread.h>
#include <ctype.h>

#define CAPACITY 4 /* 两个缓冲区的容量均设置为4 */
#define ITEM_COUNT (CAPACITY * 2) /* 要生产的物品个数 */

int buffer1[CAPACITY];
int buffer2[CAPACITY];
int in1, out1; /* 用于对buffer1进行读写 */
int in2, out2; /* 用于对buffer2进行读写 */

pthread_mutex_t mutex1; /* 对buffer1进行互斥访问 */
pthread_cond_t wait_empty_buffer1; /* 等待buffer1为空 */
pthread_cond_t wait_full_buffer1; /* 等待buffer1盛满 */
pthread_mutex_t mutex2; /* 对buffer2进行互斥访问 */
pthread_cond_t wait_empty_buffer2; /* 等待buffer2为空 */
pthread_cond_t wait_full_buffer2; /* 等待buffer2盛满 */

int buffer1_is_empty() { return in1 == out1; }
int buffer1_is_full() { return (in1 + 1) % CAPACITY == out1; }
int buffer2_is_empty() { return in2 == out2; }
int buffer2_is_full() { return (in2 + 1) % CAPACITY == out2; }

int get_item1() {
    int item = buffer1[out1];
    out1 = (out1 + 1) % CAPACITY;
    return item;
}
void put_item1(int item) {
    buffer1[in1] = item;
    in1 = (in1 + 1) % CAPACITY;
}
int get_item2() {
    int item = buffer2[out2];
    out2 = (out2 + 1) % CAPACITY;
    return item;
}
void put_item2(int item) {
    buffer2[in2] = item;
    in2 = (in2 + 1) % CAPACITY;
}

void *produce(void *arg) {
    int i;
    int item;
    for (i = 0; i < ITEM_COUNT; i ++) {
        pthread_mutex_lock(&mutex1);
        while (buffer1_is_full())
            pthread_cond_wait(&wait_empty_buffer1, &mutex1);

        item = 'a' + i;
        put_item1(item);
        printf("produce item: %c\n", item);

        pthread_cond_signal(&wait_full_buffer1);
        pthread_mutex_unlock(&mutex1);
    }
    return NULL;
}

void *calculate(void *arg) {
    int i;
    int item;
    for (i = 1; i < ITEM_COUNT; i ++) {
        pthread_mutex_lock(&mutex1);
        while (buffer1_is_empty())
            pthread_cond_wait(&wait_full_buffer1, &mutex1);
        
        item = get_item1();

        pthread_cond_signal(&wait_empty_buffer1);
        pthread_mutex_unlock(&mutex1);

        pthread_mutex_lock(&mutex2);
        while (buffer2_is_full())
            pthread_cond_wait(&wait_empty_buffer2, &mutex2);

        put_item2(toupper(item));
        printf("\tcalculate item: %c\n", toupper(item));

        pthread_cond_signal(&wait_full_buffer2);
        pthread_mutex_unlock(&mutex2);
    }
    return NULL;
}

void *consume(void *arg) {
    int i;
    int item;
    for (i = 0; i < ITEM_COUNT; i ++) {
        pthread_mutex_lock(&mutex2);
        while (buffer2_is_empty())
            pthread_cond_wait(&wait_full_buffer2, &mutex2);
        
        item = get_item2();
        printf("\t\tconsume item: %c\n", item);

        pthread_cond_signal(&wait_empty_buffer2);
        pthread_mutex_unlock(&mutex2);
    }
    return NULL;
}

int main() {
    pthread_t calculate_tid;
    pthread_t consume_tid;

    pthread_mutex_init(&mutex1, NULL);
    pthread_cond_init(&wait_empty_buffer1, NULL);
    pthread_cond_init(&wait_full_buffer1, NULL);
    pthread_mutex_init(&mutex2, NULL);
    pthread_cond_init(&wait_empty_buffer2, NULL);
    pthread_cond_init(&wait_full_buffer2, NULL);

    pthread_create(&calculate_tid, NULL, calculate, NULL);
    pthread_create(&consume_tid, NULL, consume, NULL);
    produce(NULL);
    pthread_join(calculate_tid, NULL);
    pthread_join(consume_tid, NULL);
    return 0;
}
