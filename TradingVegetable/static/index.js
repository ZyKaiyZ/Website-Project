const vm = Vue.createApp({
    delimiters: ['[[', ']]'],
    data() {
        return {
            items: [],
            count: 0,
            date: "",
            selected: "",
            down: false,
            searchMessage: "",
            menuValue: false,
            name: "",
            phone: "",
            email: "",
            message: ""
        }
    },
    methods:{
        click1: function(){
            window.location.href="/"
        },
        click2: function(){
            window.location.href="/about"
        },
        click3: function(){
            window.location.href="/contact"
        },
        click4: function(){
            axios.get('/storeData')
            .then((response)=>console.log(response.data))
            .catch((error)=>console.log(error));    
        },
        scroll: function(){
            if(this.down){
                window.scrollTo(0, 0);
                this.down=false;
            }
            else{
                window.scrollTo(0, document.body.scrollHeight);
                this.down=true;
            }
        },
        search: function(){
            axios.post('/searchData',this.searchMessage)
            .then((response)=>{
                if(response.data.length!=0){
                    vm.items=JSON.parse(JSON.stringify(response.data));
                }
                else{
                    alert("沒有資料");
                    axios.get('/getData')
                    .then(function(response){
                        vm.count=response.data.length;
                        vm.items=JSON.parse(JSON.stringify(response.data));
                        vm.date=vm.items[0][0];
                        console.log(response.data);
                    })
                    .catch((error)=>console.log(error));
                }
            })
            .catch((error)=>console.log(error));
        },
        menu: function(){
            if(this.menuValue){
                this.menuValue=false;
                console.log("out");
            }
            else{
                this.menuValue=true;
                console.log("in");
            }
        },
        selectChange: function(){
            this.sort(this.selected);
        },
        submit: function(){
            swal("成功寄出 !", "請等待我們的回覆 !", "success");
            axios.post('/getContact',
            {"name":vm.name,"phone":vm.phone,"email":vm.email,"message":vm.message})
            .then((response)=>{
                console.log(response.data);
            })
            .catch((error)=>console.log(error));
            this.name="";
            this.phone="";
            this.email="";
            this.message="";
        },
        getData(){
            console.log(this.items);
            console.log(this.count);
        },
        sort(mode){
            //[date,number,name,upper,lower,avg,volume]
            axios.post('/sortData',mode)
            .then((response)=>{
                console.log(response.data);
                vm.items=JSON.parse(JSON.stringify(response.data));
            })
            .catch((error)=>console.log(error));
        }
    },
    beforeCreate(){
        axios.get('/getData')
        .then(function(response){
            vm.count=response.data.length;
            vm.items=JSON.parse(JSON.stringify(response.data));
            vm.date=vm.items[0][0];
            console.log(response.data);
        })
        .catch((error)=>console.log(error));
    }
}).mount('#app');

