        var image_size = 1;
        const image_size_base = 50;

        function resize_image(){
            image_size = image_size % 4 + 1;
            var images = document.getElementsByName("good_image");
            for(var i=0; i<images.length; ++i){
                images[i].width = images[i].height = image_size * image_size_base;
            }
        };

        function count_down(n){
            console.log("cd");
            var input = document.getElementById("count"+n);
            var count = Number(input.value);
            if (count > 0){
                count -= 1;
                input.value = count;
                update_sum(n, count);
            }
        };

        function count_up(n){
            console.log("cu");
            var input = document.getElementById("count"+n);
            var count = Number(input.value);
            count += 1;
            input.value = count;
            update_sum(n, count);
        };

        function count_input(n){
            console.log("ci");
            var count = Number(document.getElementById("count"+n).value);
            update_sum(n, count);
        };

        function update_sum(n, count){
            console.log("us");
            var price = Number(document.getElementById("rate"+n).innerText);
            document.getElementById("sum"+n).innerText = count * price;

            var sub_sum = document.getElementsByName("sub_sum");
            var sum = 0;
            for(var i=1; i<=sub_sum.length; ++i){
                sum += Number(document.getElementById("sum"+i).innerText);
                document.getElementById("total_price").innerText = sum;
            }
        };

        function clear_cart(n){
            console.log("cc: " + n);
            var sub_sum = document.getElementsByName("sub_sum");
            if(n == 0) {
                for(var i=1; i<=sub_sum.length; ++i){
                    document.getElementById("sum"+i).innerText = 0;
                    document.getElementById("count"+i).value = 0;
                }
                document.getElementById("total_price").innerText = 0;
            }
            else {
                n = Number(n);
                var sub_sum = document.getElementsByName("sub_sum");
                var sum = 0;
                for(var i=1; i<=sub_sum.length; ++i){
                    var price = Number(document.getElementById("rate"+i).innerText);
                    document.getElementById("count"+i).value = n;
                    document.getElementById("sum"+i).innerText = n * price;
                    sum += n * price;
                    console.log("count:"+n+",price:"+price);
                }
                document.getElementById("total_price").innerText = sum;
            }
        };

        function hide_not_select() {
            var sub_sum = document.getElementsByName("sub_sum");
            for(var i=1; i<=sub_sum.length; ++i){
                count = Number(document.getElementById("count"+i).value);
                if (count <= 0){
                    document.getElementById("tr"+i).hidden = true;
                }
            }
        }

        function show_not_select() {
            var sub_sum = document.getElementsByName("sub_sum");
            for(var i=1; i<=sub_sum.length; ++i){
                document.getElementById("tr"+i).hidden = false;
            }
        }

        function httpPost(URL, PARAMS) {
            console.log("hp");
            var temp = document.createElement("form");
            temp.action = URL;
            temp.method = "post";
            temp.style.display = "none";

            for (var x in PARAMS) {
                var opt = document.createElement("textarea");
                opt.name = x;
                opt.value = PARAMS[x];
                temp.appendChild(opt);
            }

            document.body.appendChild(temp);
            temp.submit();

            return temp;
        };

        function create_order(){
            console.log("co");
            var counts = document.getElementsByName("sub_count");
            var dic = new Array();//通过申明一个Array来做一个字典
            for(var i=0; i<counts.length; ++i){
                var v = counts[i].value;
                if(v > 0){
                    dic[i] = v;
                }
            }
            httpPost("/", dic);
        };


        function all_set_rate(good_count){
            rate = Number(document.getElementById("all_rate").value);
            console.log("assr rate: " + rate)
            for(var i=1; i<=good_count; ++i){
                var price = document.getElementById("price"+i).value;
                new_price = Number(price) * Number(rate) / 100;
                console.log("price="+price+",rate="+rate+",new_price="+new_price)
                document.getElementById("rate"+i).value = new_price
            }
        };

        function ensure_modify(good_count){
            var dic = new Array();//通过申明一个Array来做一个字典
            for(var i=1; i<=good_count; ++i){
                console.log("em"+i);
                price = document.getElementById("price"+i).value;
                rate = document.getElementById("rate"+i).value;
                dic[i] = [price, rate];
            }
            httpPost("/init", dic);
        };


        function create_order_silence()
        {
            console.log("cos");
            document.getElementById("result").innerHTML = "";
            var xml_http;
            if (window.XMLHttpRequest)
            {
                //  IE7+, Firefox, Chrome, Opera, Safari 浏览器执行代码
                xml_http=new XMLHttpRequest();
            }
            else
            {
                // IE6, IE5 浏览器执行代码
                xml_http=new ActiveXObject("Microsoft.XMLHTTP");
            }
            xml_http.onreadystatechange=function()
            {
                if (xml_http.readyState==4 && xml_http.status==200)
                {
                    document.getElementById("result").innerHTML = "执行结果：" + xml_http.responseText;
                }
            }
            xml_http.open("POST", '/', true);
            xml_http.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

            var counts = document.getElementsByName("sub_count");
            var dic = new Array();//通过申明一个Array来做一个字典
            for(var i=0; i<counts.length; ++i){
                var v = counts[i].value;
                if(v > 0){
                    dic.push(String(i) + "=" + v)
                }
            }
            xml_http.send(dic.join("&"));
        };

        function add_plan() {
            console.log("aqo");
            if (document.getElementById("new_plan").value == "") {
                document.getElementById("result").innerHTML = "要生成模板，请输入模板名字";
                return;
            }

            var dic = new Array();//通过申明一个Array来做一个字典
            dic["opt"] = "add";
            dic["name"] = document.getElementById("new_plan").value;

            var counts = document.getElementsByName("sub_count");
            var temp = new Array();//通过申明一个Array来做一个字典
            for(var i=0; i<counts.length; ++i){
                temp.push(String(counts[i].value));
            }

            dic["counts"] = temp.join(",");

            httpPost("/plans", dic);
        };

        function use_plan(name) {
            console.log('up');
            var dic = new Array();//通过申明一个Array来做一个字典
            dic["opt"] = "use";
            dic["name"] = name;

            httpPost("/plans", dic);
        };

        function mod_plan(name) {
            console.log('mp');
            var dic = new Array();//通过申明一个Array来做一个字典
            dic["opt"] = "mod";
            dic["name"] = name;

            var counts = document.getElementsByName("sub_count");
            var temp = new Array();//通过申明一个Array来做一个字典
            for(var i=0; i<counts.length; ++i){
                temp.push(String(counts[i].value));
            }
            dic["counts"] = temp.join(",");

            httpPost("/plans", dic);
        };

        function del_plan(name) {
            console.log('dp');
            var dic = new Array();//通过申明一个Array来做一个字典
            dic["opt"] = "del";
            dic["name"] = name;

            httpPost("/plans", dic);
        };

        function load_plan() {
            update_sum
        }