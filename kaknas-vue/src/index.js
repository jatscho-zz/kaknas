import Vuetable from './components/Vuetable.vue'
import Promise from 'promise-polyfill'


if (!window.Promise) {
	window.Promise = Promise
}

function install(Vue){
  Vue.component("vuetable", Vuetable);
}
export {
  Vuetable,
  install
};

export default Vuetable;
