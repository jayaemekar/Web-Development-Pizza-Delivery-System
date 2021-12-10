const orders = {
    data() {
        return {
            orders: []
        }
    },
    mounted() {
        //get request
        //use results
        axios.get('/order_list/')
            .then(function (response) {
                // handle success
                restaurant_admin.order_list = response.data.order_list;
                console.log(response);
            })
            .catch(function (error) {
                // handle error
                console.log(error);
            })
        setInterval(()=>{
            axios.get('/order_list/')
            .then(function (response) {
                // handle success
                clientside.order_list = response.data.order_list;
                console.log(response);
            })
            .catch(function (error) {
                // handle error
                console.log(error);
            })
        }, 10000);

    }

}

restaurant_admin = Vue.createApp(orders).mount('#list-rendering')