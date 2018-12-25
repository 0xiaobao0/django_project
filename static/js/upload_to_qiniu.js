function ajaxform() {
    var formData = new FormData();
    formData.append('file', document.getElementById('file').files[0]);
    formData.append('key', document.getElementById('key').value);
    formData.append('token', document.getElementById('token').value);

    $.ajax({
        url: 'http://up-z1.qiniup.com/',
        data: formData,
        type: "POST",
        contentType: false,//这里
        processData: false,//这两个一定设置为false

        success: function (data) {
            url = 'http://'+'img.hellowmrliu.cn/'+data['key'];
            setdata(url)
        }
        // error:function(){
        //     alert('图片上传失败');
        // }
    })
}
function setdata(imgurl) {
    document.getElementById('img_url').value = imgurl
}
