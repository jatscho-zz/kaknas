var section = document.querySelector('section');
var article = document.createElement('article');
projectTable = document.getElementById('projects');
projectTitle = document.getElementById('projectTitles');
function getDiff(module, greenfield_commit_sha, other_commit_sha, moduleRefCell) {
  $.ajax({
        url: '/diff_check',
        type: 'post',
        dataType: 'json',
        contentType: 'application/json;charset=UTF-8',
        data: JSON.stringify({[module] : { [greenfield_commit_sha] : other_commit_sha } }),
        success: function (data) {
          if (data == 'False') {
            moduleRefCell.style.color = 'red';
          } else if (data == 'True') {
            moduleRefCell.style.color = 'black';
          }
        },
    });
}
function populateModuleInfo(module_state_map) {
  for (var module in module_state_map) {
    var greenfield_commit_sha = null;
    var equinor_commit_sha = null;
    var west1_commit_sha = null;
    var moduleRefCell = null;
    var moduleRefCellEquinor = null;
    var moduleRefCellWest = null;
    var moduleRow = document.createElement('tr');
    var moduleCell = document.createElement('td');
    moduleCell.textContent = module;
    moduleRow.append(moduleCell);
    module_info = module_state_map[module];
    var modulePathCell = document.createElement('td');
    var modulePathList = document.createElement('ul');
    for (var module_path in module_info) {
      var singleModulePath = document.createElement('li');
      singleModulePath.textContent = module_path;
      modulePathList.append(singleModulePath);
      modulePathCell.append(modulePathList);
      moduleRow.append(modulePathCell);
    }
    for (var module_path in module_info) {
      for (var project in module_info[module_path]) {
        var project_info = module_info[module_path][project];
        if (project == 'cognitedata-greenfield') {
            moduleRefCell = document.createElement('td');
            greenfield_commit_sha = project_info[Object.keys(project_info)[0]]
            moduleRefCell.textContent = Object.keys(project_info)[0] + " : " + greenfield_commit_sha;
            moduleRow.append(moduleRefCell);
        } else if (project == 'cognitedata-equinor') {
            equinor_commit_sha = project_info[Object.keys(project_info)[0]]
            moduleRefCellEquinor = document.createElement('td');
            moduleRefCellEquinor.textContent = Object.keys(project_info)[0] + " : " + equinor_commit_sha;
            moduleRow.append(moduleRefCellEquinor);
        } else if (project == 'cognitedata-europe-west1-1') {
            west1_commit_sha = project_info[Object.keys(project_info)[0]]
            moduleRefCellWest = document.createElement('td');
            moduleRefCellWest.textContent = Object.keys(project_info)[0] + " : " + west1_commit_sha;
            moduleRow.append(moduleRefCellWest);
        }
      }
    }
    if (equinor_commit_sha && greenfield_commit_sha != equinor_commit_sha) {
      getDiff(Object.keys(project_info)[0], greenfield_commit_sha, equinor_commit_sha, moduleRefCellEquinor);
    }
    if (west1_commit_sha && greenfield_commit_sha != west1_commit_sha) {
      getDiff(Object.keys(project_info)[0], greenfield_commit_sha, west1_commit_sha, moduleRefCellWest);
    }
    projects.append(moduleRow);
  }
}
