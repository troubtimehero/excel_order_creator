        var xml_http;
        var image_size = 1;
        const image_size_base = 50;
        const sell_form_ids = new Array('sf_company', 'sf_tel', 'sf_customer', 'sf_address', 'sf_order_no', 'sf_salesman');

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
            }
            document.getElementById("total_price").innerText = sum;
        };

        function cal_all() {
            console.log("ca");
            var sub_sum = document.getElementsByName("sub_sum");
            var sum = 0;
            for(var i=1; i<=sub_sum.length; ++i){
                var price = Number(document.getElementById("rate"+i).innerText);
                var count = Number(document.getElementById("count"+i).value);
                document.getElementById("sum"+i).innerText = count * price;
                sum += price * count;
            }
            document.getElementById("total_price").innerText = sum;
        }

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
                for(var i=1; i<=sub_sum.length; ++i){
                    document.getElementById("count"+i).value = n;
                }
                cal_all();
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
            httpPost("/order_creator", dic);
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
            httpPost("/order_creator/init", dic);
        };


        function create_order_silence(opt)
        {
            var btns = document.getElementsByName("btn_create_order");
            for(var i=0; i<btns.length; ++i){
                btns[i].disabled = true;
            }
            setTimeout(function(){
                var btns = document.getElementsByName("btn_create_order");
                for(var i=0; i<btns.length; ++i){
                    btns[i].disabled = false;
                }
            }, 2000);


            console.log("cos");
            document.getElementById("result").innerHTML = "";
            if (window.XMLHttpRequest)
            {
                //  IE7+, Firefox, Chrome, Opera, Safari 浏览器执行代码
                xml_http = new XMLHttpRequest();
            }
            else
            {
                // IE6, IE5 浏览器执行代码
                xml_http = new ActiveXObject("Microsoft.XMLHTTP");
            }
            xml_http.onreadystatechange = function()
            {
                if (xml_http.readyState==4 && xml_http.status==200)
                {
                    document.getElementById("result").innerHTML = "订单已生成：";
                    dl = document.getElementById("link_download");
                    dl.href = xml_http.responseText;
                    dl.hidden = false;
                }
            }
            xml_http.open("POST", '/order_creator', true);
            xml_http.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

            var counts = document.getElementsByName("sub_count");
            var dic = new Array();//通过申明一个Array来做一个字典
            for(var i=0; i<counts.length; ++i){
                var v = counts[i].value;
                if(v > 0){
                    dic.push(String(i) + "=" + v);
                }
            }
            dic.push("opt="+opt);

            for(i=0; i<sell_form_ids.length; ++i){
                inp = document.getElementById(sell_form_ids[i]).value;
                if(inp != ""){
                    dic.push(sell_form_ids[i] + "=" + inp);
                }
            }

            xml_http.send(dic.join("&"));

            document.getElementById("result").innerHTML = "运算中...";
            document.getElementById("link_download").hidden = true;
        };

// ///////////////////////////////////////////////////// plan

        function ajax(url, params, callback)
        {
            console.log("ajax");
            if (window.XMLHttpRequest)
            {
                //  IE7+, Firefox, Chrome, Opera, Safari 浏览器执行代码
                xml_http = new XMLHttpRequest();
            }
            else
            {
                // IE6, IE5 浏览器执行代码
                xml_http = new ActiveXObject("Microsoft.XMLHTTP");
            }
            xml_http.onreadystatechange = callback;
            xml_http.open("POST", url, true);
            xml_http.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
            xml_http.send(params);
        };

        function auto_hide_tips(id, tips){
            console.log(id + tips);
            document.getElementById(id).innerHTML = tips;
            setTimeout(function(){document.getElementById(id).innerHTML = "";}, 3000);
        }


        function add_plan() {
            console.log("aqo");
            if (document.getElementById("new_plan").value == "") {
                auto_hide_tips("result_plans", "必须输入模板名字");
                return;
            }

            var dic = new Array();//通过申明一个Array来做一个字典
            dic["opt"] = "add";
            dic["name"] = document.getElementById("new_plan").value;

            old_plans = document.getElementsByName("plan_name");
            for (var i=0; i<old_plans.length; ++i){
                if(old_plans[i].innerText == dic["name"]){
                    auto_hide_tips("result_plans", "模板名字不能重复");
                    return;
                }
            }

            var counts = document.getElementsByName("sub_count");
            var temp = new Array();//通过申明一个Array来做一个字典
            for(var i=0; i<counts.length; ++i){
                temp.push(String(counts[i].value));
            }

            dic["counts"] = temp.join(",");

            httpPost("/order_creator/plans", dic);
        };

        function use_plan(name) {
            console.log('up');
            ajax("/order_creator/plans", "opt=use&name="+name, function(){
                if (xml_http.readyState==4 && xml_http.status==200)
                {
                    rt_w = JSON.parse(xml_http.responseText);
                    var counts = document.getElementsByName("sub_count");
                    for(var i=0; i<counts.length; ++i){
                        counts[i].value = rt_w[i];
                    }

                    cal_all();
                }
            });
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

            httpPost("/order_creator/plans", dic);
        };

        function del_plan(name) {
            console.log('dp');
            var dic = new Array();//通过申明一个Array来做一个字典
            dic["opt"] = "del";
            dic["name"] = name;

            httpPost("/order_creator/plans", dic);
        };

        function load_plan() {
            console.log("lp");
            cal_all();
//            setTimeout(cal_all, 1000);
        };

        var hide_plan_div = false;
        function plan_div(div, btn, show, hide) {
            console.log('pd');
            hide_plan_div = !hide_plan_div;
            document.getElementById(div).hidden = hide_plan_div;
            if (hide_plan_div){
                document.getElementById(btn).innerText = show; // "模板>>";
            }
            else{
                document.getElementById(btn).innerText = hide; // "<<隐藏";
            }
        };


// ///////////////////////////////////////////////////// customer


        function add_customer() {
            console.log("ac");
            if (document.getElementById("sf_company").value == "") {
                auto_hide_tips("result_customer", "必须请输入收货单位");
                return;
            }

            var dic = new Array();//通过申明一个Array来做一个字典
            dic["opt"] = "add";
            dic["name"] = document.getElementById("sf_company").value;

            old_plans = document.getElementsByName("customer_name");
            for (var i=0; i<old_plans.length; ++i){
                if(old_plans[i].innerText == dic["name"]){
                    auto_hide_tips("result_customer", "单位名字不能重复");
                    return;
                }
            }

            for (var i=0; i<sell_form_ids.length; ++i){
                dic[sell_form_ids[i]] = document.getElementById(sell_form_ids[i]).value;
            }

            httpPost("/order_creator/customer", dic);
        };

        function use_customer(name) {
            console.log('uc');
            ajax("/order_creator/customer", "opt=use&name="+name, function(){
                if (xml_http.readyState==4 && xml_http.status==200)
                {
                    //更新数据
                    rt_w = JSON.parse(xml_http.responseText);
                    for(i=0; i<sell_form_ids.length; ++i){
                        document.getElementById(sell_form_ids[i]).value = rt_w[sell_form_ids[i]];
                    }
                }
            });
        };

        function mod_customer(name) {
            console.log('mc');
            var dic = new Array();//通过申明一个Array来做一个字典
            dic["opt"] = "mod";
            dic["name"] = name;

            for (var i=0; i<sell_form_ids.length; ++i){
                dic[sell_form_ids[i]] = document.getElementById(sell_form_ids[i]).value;
            }

            httpPost("/order_creator/customer", dic);
        };

        function del_customer(name) {
            console.log('dc');
            var dic = new Array();//通过申明一个Array来做一个字典
            dic["opt"] = "del";
            dic["name"] = name;

            httpPost("/order_creator/customer", dic);
        };

    function forbid_outnet(){
        var fb = "no";
        if(document.getElementById('forbid').checked)
        {
            fb = "yes";
        }
        ajax("/order_creator/forbid", "forbid="+fb, function(){});
    };