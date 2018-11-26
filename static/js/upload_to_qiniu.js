function ajaxform() {
    var formData = new FormData();
    formData.append('file', document.getElementById('file').files[0]);
    formData.append('key', document.getElementById('key').value);
    formData.append('token', document.getElementById('token').value);

    // var formData2 = new FormData();
    // formData.append('file', document.getElementById('file').files[0]);
    // formData2.append('towho', document.getElementById('towho').value);
    // formData2.append('anonymous', document.getElementById('anonymous').value);
    // formData2.append('content', document.getElementById('content').value);

    $.ajax({
        url: 'http://up-z1.qiniup.com/',
        data: formData,
        type: "POST",
        contentType: false,//这里
        processData: false,//这两个一定设置为false

        success: function (data) {
            // $.ajax({
            //     url: 'http://0smallwhite0.vicp.io:16991/declare',
            //     data: formData,
            //     type: "POST",
            //     contentType: false,//这里
            //     processData: false,//这两个一定设置为false
            //
            //     success: function () {
            //         alert('成功');
            //     },
            //     error:function(){
            //         alert('图片上传失败');
            //     }
            // })
            // var result = JSON.parse(data);
            url = 'img.hellowmrliu.cn/'+data['key'];
            setdata(url)
            // console.log(url);
            // alert(url)
        },
        error:function(){
            alert('图片上传失败');
        }
    })
}
function setdata(imgurl) {
    document.getElementById('img_url').value = imgurl

}
        // <input name="towho" id="towho" type="text"></br>
        // <input name="anonymous" id="anonymous" type="text"></br>
        // <input name="content" id="content" type="text"></br>