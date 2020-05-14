<?php
if(empty($_POST)){
    get_html();
}

if(empty($_POST['name'])){
    get_html('名字不能为空');
}elseif($_POST['type'] == 'plugin' && empty($_POST['remarks']) && empty($_POST['remarks_cn'])){
    get_html('备注不能为空');
}elseif(empty($_POST['raw_url_cn']) or empty($_POST['raw_url'])){
    get_html('下载地址不能为空');
}elseif(empty($_POST['file'])){
    get_html('文件名不能为空');
}elseif(empty($_POST['author'])){
    get_html('作者不能为空');
}

function get_html($error=''){
    if(empty($error)){
    $json = file_get_contents('https://raw.githubusercontent.com/Squaregentleman/MCDR-get/master/list.json');
    $json_jx = json_decode($json,true);
    print('<head> 
    <meta http-equiv="content-Type" content="text/html; charset=utf-8">
</head>
<style>
    body {TEXT-ALIGN: center;}
</style>
<body>
<form action="index.php" method="post">
    <p>类型: <select name="type">
        <option value="plugin">插件</option>
        <option value="api">Api</option>
        </select>
    <p>名字: <input type="text" name="name" /></p>
    <p>备注(Api不用写)(中文): <input type="text" name="remarks_cn" /></p>
    <p>备注(Api不用写)(英文): <input type="text" name="remarks" /></p>
    <p>下载地址(国内): <input type="text" name="raw_url_cn" /></p>
    <p>下载地址(国外): <input type="text" name="raw_url" /></p>
    <p>插件调用api(Api不用写)(没调用不用写): <input type="text" name="lib" /></p>
    <p>python调用库(Api不用写)(默认安装的不用写): <input type="text" name="pip_lib" /></p>
    <p>文件名(全称+后缀): <input type="text" name="file" /></p>
    <p>作者: <input type="text" name="author" /></p>
    <p>旧json(首次生成无需填写): <input type="text" name="json" /></p>
    <input type="submit" value="提交" />
  </form>
</body>
当前json内容:<br/>
<textarea>'.htmlentities(json_encode($json_jx,JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT|JSON_UNESCAPED_SLASHES)).'</textarea>');
exit();
    }else{
        print('<head> 
    <meta http-equiv="content-Type" content="text/html; charset=utf-8">
</head>
<style>
    body {TEXT-ALIGN: center;}
</style>
<body>
错误: '.$error.'</br>
<input type="button" name="Submit" onclick="javascript:history.back(-1);" value="返回">
</body>');
exit();
    }
}

if(empty($_POST['json'])){
    $json = file_get_contents('https://raw.githubusercontent.com/Squaregentleman/MCDR-get/master/list.json');
    $json_jx = json_decode($json,true);
}else{
    $json_jx = json_decode($_POST['json'],true);
}
if($_POST['type'] == 'plugin'){
    if(strpos($_POST['lib'], ',') != False){
        $lib = explode(',', $_POST['lib']);
    }else{
        if(!empty($_POST['lib'])){
            $lib = array($_POST['lib']);
        }else{
            $lib = array();
        }
    }
    if(strpos($_POST['pip_lib'], ',') != False){
        $pip_lib = explode(',', $_POST['pip_lib']);
    }else{
        if(!empty($_POST['pip_lib'])){
            $pip_lib = array($_POST['pip_lib']);
        }else{
            $pip_lib = array();
        }
        
    }
    if($_POST['raw_url_cn'] == ''){
        $url = $_POST['raw_url'];
    }else{
        $url = $_POST['raw_url_cn'];
    }
    if($_POST['raw_url_cn'] == ''){
        $url2 = $_POST['raw_url_cn'];
    }else{
        $url2 = $_POST['raw_url'];
    }
    $array = array(
        'name' => $_POST['name'],
        'remarks_cn' => $_POST['remarks_cn'],
        'remarks' => $_POST['remarks'],
        'raw_url_cn' => $url,
        'raw_url' => $url2,
        'lib' => $lib,
        'pip_lib' => $pip_lib,
        'file' => $_POST['file'],
        'author' => $_POST['author'],
    );
    $json_jx['list'] = array_merge($json_jx['list'], array($array));
    $json_jx['time'] = time();
        print('<head> 
    <meta http-equiv="content-Type" content="text/html; charset=utf-8">
</head>
<style>
    body {TEXT-ALIGN: center;}
</style>
<body>
<form action="index.php" method="post">
    <p>类型: <select name="type">
        <option value="plugin">插件</option>
        <option value="api">Api</option>
        </select>
    <p>名字: <input type="text" name="name" /></p>
    <p>备注(Api不用写)(中文): <input type="text" name="remarks_cn" /></p>
    <p>备注(Api不用写)(英文): <input type="text" name="remarks" /></p>
    <p>下载地址(国内): <input type="text" name="raw_url_cn" /></p>
    <p>下载地址(国外): <input type="text" name="raw_url" /></p>
    <p>插件调用api(Api不用写)(没调用不用写): <input type="text" name="lib" /></p>
    <p>python调用库(Api不用写)(默认安装的不用写): <input type="text" name="pip_lib" /></p>
    <p>文件名: <input type="text" name="file" /></p>
    <p>作者: <input type="text" name="author" /></p>
    <p>旧json(如果需要继续添加插件继续写就行): <input type="text" name="json" value="'.htmlentities(json_encode($json_jx)).'" /></p>
    <input type="submit" value="提交" />
  </form>
</body>
生成的json内容(ctrl+a全选复制):<br/>
<textarea>'.htmlentities(json_encode($json_jx)).'</textarea>');
}elseif($_POST['type'] == 'api'){
    $array = array(
        'name' => $_POST['name'],
        'raw_url_cn' => $_POST['raw_url_cn'],
        'raw_url' => $_POST['raw_url'],
        'file' => $_POST['file'],
        'author' => $_POST['author'],
    );
    $json_jx['api_list'] = array_merge($json_jx['api_list'], array($array));
    $json_jx['time'] = time();
        print('<head> 
    <meta http-equiv="content-Type" content="text/html; charset=utf-8">
</head>
<style>
    body {TEXT-ALIGN: center;}
</style>
<body>
<form action="index.php" method="post">
    <p>类型: <select name="type">
        <option value="plugin">插件</option>
        <option value="api">Api</option>
        </select>
    <p>名字: <input type="text" name="name" /></p>
    <p>备注(Api不用写)(中文): <input type="text" name="remarks_cn" /></p>
    <p>备注(Api不用写)(英文): <input type="text" name="remarks" /></p>
    <p>下载地址(国内): <input type="text" name="raw_url_cn" /></p>
    <p>下载地址(国外): <input type="text" name="raw_url" /></p>
    <p>插件调用api(Api不用写)(没调用不用写): <input type="text" name="lib" /></p>
    <p>python调用库(Api不用写)(默认安装的不用写): <input type="text" name="pip_lib" /></p>
    <p>文件名: <input type="text" name="file" /></p>
    <p>作者: <input type="text" name="author" /></p>
    <p>旧json(如果需要继续添加插件继续写就行): <input type="text" name="json" value="'.htmlentities(json_encode($json_jx)).'" /></p>
    <input type="submit" value="提交" />
  </form>
</body>
生成的json内容(ctrl+a全选复制):<br/>
<textarea>'.htmlentities(json_encode($json_jx)).'</textarea>');
}
