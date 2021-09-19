# 可能他又对了
```go
package main

import (
	"fmt"
	"github.com/google/gopacket"
	"github.com/google/gopacket/layers"
	"github.com/google/gopacket/pcap"
	"log"
	"time"
)

func main() {

	devices, err := pcap.FindAllDevs() //不知道为啥，用这个API得到的就不是中文,我自己写的得到的网卡名就是中文
	if err != nil {
		log.Fatal(err)
	}

	interfaceNames := []string{}
	for _, device := range devices {
		for _, addr := range device.Addresses {
			if addr.IP.IsLoopback() ||
				addr.IP.IsMulticast() ||
				addr.IP.IsUnspecified() ||
				addr.IP.IsLinkLocalUnicast() {
				//不知道这些类型的网卡要不要过滤
				continue
			}
			interfaceNames = append(interfaceNames, device.Name)
		}
	}

	fmt.Println("InterFace:", interfaceNames)
	PacketChanList := []chan gopacket.Packet{}
	for _, name := range interfaceNames {
		handle, err := pcap.OpenLive(name, 1024, true, 2*time.Second)
		defer handle.Close()
		if err != nil {
			fmt.Printf("pcap open live failed: %v", err)
			return
		}
		packetSource := gopacket.NewPacketSource(handle, handle.LinkType())
		PacketChanList = append(PacketChanList, packetSource.Packets())
	}

	parseICMP:=func (pChan chan gopacket.Packet) {
		for packet:=range pChan{
			ipLayer := packet.Layer(layers.LayerTypeIPv4)
			if ipLayer != nil {
				icmpLayer := packet.Layer(layers.LayerTypeICMPv4)
				if icmpLayer != nil {
					//todo:用json的包在这里Dump你想要的结构化的数据
					fmt.Println(icmpLayer.LayerType())
					fmt.Println(string(icmpLayer.LayerPayload()))
					fmt.Println(icmpLayer)
				}
			}
		}
	}

	//todo：这里的轮询写的不知道对不对
	for _,pChan:=range PacketChanList{
		select {
		case  <-pChan:
			parseICMP(pChan)
		}
	}

}

```
