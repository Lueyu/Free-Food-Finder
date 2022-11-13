import Vue from 'vue'
import App from './App.vue'
import router from './router'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import locale from './en.js'
import * as VueGoogleMaps from "vue2-google-maps"
Vue.config.productionTip = false

Vue.use(ElementUI, { locale });
Vue.use(VueGoogleMaps, {
  load: {
    key: "AIzaSyBjXGFxHGJASTC-Fu3QM6EUp5wSWhCIfRQ",
    libraries: "places"
  }
});
new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
