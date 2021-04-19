## 1.download && install
[官网下载](https://golang.org/dl/)
安装
```shell
sudo tar -C /usr/local -xzf g
export PATH=$PATH:/usr/local/go/bin
go versio
```

## VSCode配置
搜索安装Go官方插件；
设置中搜索go: delve, 
settings.json设为：

```json
{
    "code-runner.runInTerminal": true,
    "window.zoomLevel": 1,
    "go.delveConfig": {


        "dlvLoadConfig": {
            "followPointers": true,
            "maxVariableRecurse": 1,
            "maxStringLen": 64,
            "maxArrayValues": 64,
            "maxStructFields": -1
        },
        "apiVersion": 2,
        "showGlobalVariables": false,
        "debugAdapter": "legacy"
    },
    "go.useCodeSnippetsOnFunctionSuggest": true,
    "go.autocompleteUnimportedPackages": true,
    "go.goroot": "/usr/local/go",
    "go.useCodeSnippetsOnFunctionSuggestWithoutType": true,
    "go.inferGopath": true,
    "go.gotoSymbol.includeImports": true,
    "go.gotoSymbol.includeGoroot": true,
    "go.formatTool": "gofmt"
}
```

## 重要！重启
重启后，打开vscode，ctrl+shift+p，
```go
Go:Install/Update Tools
```
回显：All tools successfully installed. You're ready to Go :)