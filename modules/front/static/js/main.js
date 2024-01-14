const GITHUB_MASTER_URL = 'https://raw.githubusercontent.com/katomaro/katomart/master';
const GITHUB_VERSION_URL = `${GITHUB_MASTER_URL}/VERSIONS.json`;
const GITHUB_MESSAGE_URL = `${GITHUB_MASTER_URL}/AVISO.html`;


// Json com a versão dos scripts carregadas do Github
let versions = null;
function loadVersions() {
    $.ajax({
        url: GITHUB_VERSION_URL,
        type: "GET",
        dataType: "json",
        success: function(data) {
            versions = data;
        },
        error: function() {
            versions = {};
        }
    });
}