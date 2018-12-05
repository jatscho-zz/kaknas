import Vue from 'vue'
import Vuetable from './components/Vuetable.vue'
import { Badge } from 'bootstrap-vue/es/components';
import { Button } from 'bootstrap-vue/es/components';

Vue.use(Button);
Vue.use(Badge);
let E_SERVER_ERROR = 'Error communicating with the server'


Vue.component('custom-actions', {
  template: [
    '<div>',
      '<button class="ui green button" @click="onClick(\'view-item\', rowData)"><i class="zoom icon"></i></button>',
    '</div>'
  ].join(''),
  props: {
    rowData: {
      type: Object,
      required: true
    }
  },
  data: {
    moduleInfo: {}
  },
  methods: {
    onClick (action, data) {
      console.log('actions: on-click', data)
      for (var key in data) {
        if (key != 'id' && key != 'module_name') {
          this.moduleInfo[key] = {}
          this.moduleInfo[key]["git_ref"] = data[key]["git_ref"]
          this.moduleInfo[key]["module_source"] = data[key]["module_source"]
          this.moduleInfo[key]["path_to_module"] = data[key]["path_to_module"]
          console.log(this.moduleInfo)
        }
      }
      const node1 = (`<li v-for="(item, key) in moduleInfo"> {{ item }} - {{ key }} </li>`)
      const node = (`<li> {{ item }} - {{ key }} </li>`)
      swal({
        title: data.module_name,
        content:
          `${node1}`,
      });
    },
  },
  mounted(){
    this.moduleInfo = {}
  },
})

Vue.component('my-detail-row', {
  template: [
    '<ul>',
      '<li v-for="commit_info in getModuleCommits(rowData.module_name)">',
        '<a target="_blank" :href="`${getCommitLink(commit_info.sha_commit)}`" class="commit">{{ commit_info.sha_commit.slice(0, 7) }}</a>',
        ' - <span class="message">{{ commit_info.description }}</span>',
        ' by <span class="author">{{ getAuthor(commit_info.committer) }} </span>',
        '<b-badge v-if="isGreenfield(rowData.module_name, commit_info.sha_commit)" variant="success">',
          'Greenfield',
        '</b-badge>',
        '<b-badge v-if="isEquinor(rowData.module_name, commit_info.sha_commit)" variant="danger">',
          'Equinor',
        '</b-badge>',
        '<b-badge v-if="isWest1(rowData.module_name, commit_info.sha_commit)" variant="primary">',
          'West-1',
        '</b-badge>',
      '</li>',
    '</ul>'
  ].join(''),

  //   '<div @click="onClick">',
  //     '<div class="inline field">',
  //       '<h4>Module: <a :href="`${getModulePath(rowData)}`" > {{ rowData.module_name }} </a></h4>',
  //       '<br>',
  //       '<span v-for="(projectObj, project) in filterKeys(rowData)">',
  //         '<div class="col-md-12">',
  //           '<div class="col-md-4 pb-2">{{ project }} : <a target=_blank :href="`${getCommitPath(projectObj.git_ref)}`  "> {{ projectObj.git_ref }}</a> </div>',
  //           '<a class="col-md-4 pb-2" target=_blank :href="`${getComparePath(projectObj.git_ref)}`">',
  //             '<button v-if="isNotGreenfield(project)" class="ui green button" >',
  //               'Git compare with Greenfield',
  //             '</button>',
  //           '</a>',
  //         '</div>',
  //         '<br>',
  //       '</span>',
  //     '</div>',
  //   '</div>'
  // ].join(''),
  props: {
    rowData: {
      type: Object,
      required: true
    },
    commitData: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      greenfield_commit_map : {},
      cognite_modules_url : 'https://github.com/cognitedata/terraform-cognite-modules/',
      compare_cognite_modules_url: 'https://github.com/cognitedata/terraform-cognite-modules/compare/',
      commits: null,
    }
  },
  methods: {
    onClick (event) {
      console.log('my-detail-row: on-click', event.target)
      console.log('dataow: on-click', this.rowData)
    },
    getModuleCommits(moduleAtRow) {
      if (this.commitData[moduleAtRow] != null) {
        return this.commitData[moduleAtRow]["module_commits"]
      }
      return []
    },
    getAuthor(authorString) {
      return authorString.split(" ")[1]
    },
    getCommitLink(commit) {
      return this.cognite_modules_url + 'commit/' + commit
    },
    filterKeys(rowData) {
      return Object.keys(this.rowData).reduce(
        (result, key) =>
          key != 'id' && key!= 'module_name' && key != 'module_source'
            ? Object.assign(result, { [key]: rowData[key]})
            : result,
        {}
      )
    },
    isGreenfield(module, commit) {
      return this.commitData[module]['cognitedata-greenfield'] == commit
    },
    isEquinor(module, commit) {
      return this.commitData[module]['cognitedata-equinor'] == commit
    },
    isWest1(module, commit) {
      return this.commitData[module]['cognitedata-europe-west1-1'] == commit
    },
    getModulePath(rowData) {
      for (var project in rowData) {
        if (project != 'id' && project != 'module_name') {
          return this.cognite_modules_url + 'tree/master/' + rowData[project]["module_source"]
        }
      }
    },
    getCommitPath(commit) {
      return this.cognite_modules_url + 'commit/' + commit
    },
    getComparePath(commit) {
      if (this.rowData["cognitedata-greenfield"] == null) { return null }
      return this.compare_cognite_modules_url + commit + '...' + this.rowData["cognitedata-greenfield"]["git_ref"]
    },
    isNotGreenfield(project) {
      return this.rowData["cognitedata-greenfield"] && project != 'cognitedata-greenfield'
    }
  }
})

Vue.component('settings-modal', {
  template: `
    <div class="ui small modal" id="settingsModal">
      <div class="content ui form">
        <div class="ui divider"></div>
        <div class="ui fluid card">
          <div class="content">
            <div class="header">Filter projects</div>
          </div>
          <div v-if="vuetableFields" class="content">
            <div v-for="(field, idx) in vuetableFields.slice(4, vuetableFields.length)" class="field">
              <div class="ui checkbox">
                <input type="checkbox" :checked="field.visible" @change="toggleField(idx + 4, $event)">
                <label>{{ field.title }}</label>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="actions">
        <div class="ui cancel button">Close</div>
      </div>
    </div>
  `,
  props: ['vuetableFields'],
  data () {
    return {
    }
  },
  methods: {
    toggleField (index, event) {
      this.$parent.$refs.vuetable.toggleField(index)
    },
  }
})

let tableColumns = [
  {
    name: '__sequence',
    title: 'No.',
    titleClass: 'right aligned',
    dataClass: 'right aligned',
    width: '50px',
  },
  {
    name: 'module_source',
    title: 'Module Source',
    titleClass: 'text-left',
    dataClass: 'text-left',
    sortField: 'module_source',
    width: '250px',
  },
  {
    name: 'module_name',
    title: 'Module',
    titleClass: 'text-left',
    dataClass: 'text-left',
    //sortField: 'module_name',
    width: '250px',
  },
  {
    name: 'cognitedata-greenfield',
    title: 'Greenfield',
    titleClass: 'text-center',
    dataClass: 'text-left',
    //sortField: 'cognitedata-greenfield',
    callback: 'git_ref'
  },
  {
    name: 'cognitedata-equinor',
    title: 'Equinor',
    titleClass: 'text-center',
    dataClass: 'text-left',
    //sortField: 'cognitedata-equinor',
    callback: 'git_ref'
  },
  {
    name: 'cognitedata-europe-west1-1',
    title: 'West-1',
    titleClass: 'text-center',
    dataClass: 'text-left',
    //sortField: 'cognitedata-europe-west1-1',
    callback: 'git_ref'
  },
  {
    name: 'cognitedata-production',
    title: 'Production',
    titleClass: 'text-center',
    dataClass: 'text-left',
    //sortField: 'cognitedata-production',
    callback: 'git_ref'
  },
  {
    name: 'cognitedata-development',
    title: 'Development',
    titleClass: 'text-center',
    dataClass: 'text-left',
    //sortField: 'cognitedata-development',
    callback: 'git_ref'
  },
  {
    name: 'cognitedata-test',
    title: 'Test',
    titleClass: 'text-center',
    dataClass: 'text-left',
    //sortField: 'cognitedata-test',
    callback: 'git_ref'
  },
  // {
  //   name: '__component:custom-actions',
  //   title: '',
  //   titleClass: 'center aligned',
  //   dataClass: 'center aligned',
  //   width: '150px'
  // }
]

/* eslint-disable no-new */
let vm = new Vue({
  el: '#app',
  components: {
    Vuetable,
  },
  data: {
    loading: '',
    moduleInfo: false,
    fields: tableColumns,
    vuetableFields: false,
    test: [{
        field: 'module_source',
        direction: 'asc',
    }],
    multiSort: false,
  },

  methods: {
    showSettingsModal () {
      let self = this
      $('#settingsModal').modal({
        detachable: true,
        onVisible () {
          $('.ui.checkbox').checkbox()
        }
      }).modal('show')
    },
    git_ref (value) {
      for (var key in value) {
        if (key == 'git_ref') {
          return value[key]
        }
      }
    },
    showLoader () {
      this.loading = 'loading'
    },
    hideLoader () {
      this.loading = ''
    },
    showDetailRow (value) {
      let icon = this.$refs.vuetable.isVisibleDetailRow(value) ? 'down' : 'right'
      return [
        '<a class="show-detail-row">',
            '<i class="chevron circle ' + icon + ' icon"></i>',
        '</a>'
      ].join('')
    },
    rowClassCB (data, index) {
      return (index % 2) === 0 ? 'odd' : 'even'
    },
    onCellClicked (data, field, event) {
      console.log('cellClicked', field.name)
      if (field.name !== '__actions') {
        this.$refs.vuetable.toggleDetailRow(data.id)
      }
    },
    onCellDoubleClicked (data, field, event) {
      console.log('cellDoubleClicked:', field.name)
    },
    onCellRightClicked (data, field, event) {
      console.log('cellRightClicked:', field.name)
    },
    onInitialized (fields) {
      console.log('onInitialized', fields)
      this.vuetableFields = fields
      this.moduleInfo = fields
    },
    onDataReset () {
      console.log('onDataReset')
      this.$refs.paginationInfo.resetData()
      this.$refs.pagination.resetData()
    },

  },
})
