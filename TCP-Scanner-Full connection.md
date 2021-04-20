# TCP-Scanner | 全连接
## 1.**Go语言的Net包提供DialTimeout函数**
![](/uploads/upload_d70b2e8541d7e1f1addf0849cc40e0b6.png)
利用该函数，实现一个判断端口是否存在的方法：
```go
package main
import (
	"fmt"
	"net"
)
//如果出书，这里会判断error!=nil后的处理啥的，但自己写也就图一乐
func main() {
	fmt.Print(net.Dial("tcp", "152.136.116.14:80"))
}
```
### 结果：
能连我服务器的80端口，连不了8013（因为我没开），行。
![](http://l1q.design:1023/uploads/upload_33314f20b87e2856aead3d8938922171.png)

## 2.多个IP与端口：引入库 *iprange* | 单线程 垃圾
iprange库可以parse Nmap类型的IP成为 AddressRange对象；
我们可以调用AddressRange的Expand方法返回一个[]net.IP
### 代码见github
主要是Parse的过程，无聊
### 结果：
![](http://l1q.design:1023/uploads/upload_b49883d38823d79108ebd7eba98cb8b4.png)
太慢

## 3. 支持并发的TCP-全连接
### 实现过程
1）Parse。 Parse出IP和Port的slice，然后构造一个[ ]map[string] int, 其中{key-IP:value-Port}，用以表示IP和port对
2）Divide。 根据并发数，讲[]map[string]int分组
3）Divide&Conquer。按组执行扫描。 扫描任务利用*sync.WaitGroup*实现并发；将结果保存到一个**并发安全**的map中
4）show。 输出结果
### 过程3）的代码
由于通过sync.WaitGroup控制concurrency,程序将一次性创建所有协程，然后等待所有任务完成。
```go
func RunTask(tasks []map[string]int) {
	var wg sync.WaitGroup
	wg.Add(len(tasks))
	// 每次创建len(tasks)个goroutine，每个goroutine只处理一个ip:port对的检测
	for _, task := range tasks {
		for ip, port := range task {
			go func(ip string, port int) {
				err := SaveResult(Connect(ip, port))
				_ = err
				wg.Done()
			}(ip, port)
		}
	}
	wg.Wait()
}
```
### 改进
过程3）对协程的控制粒度不够细，每组扫描任务会瞬间启动大量协程然后关闭；
为解决此问题，可以使用*channel*和sync.WaitGroup配合
（生产消费者问题）

### 结果
有点小问题，但多扫几遍能扫出来，行
![](http://152.136.116.14:1023/uploads/upload_f59bd8acc9a4925bccd5b7898c495b17.png)