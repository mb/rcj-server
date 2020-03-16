const LS_DATA = "rcj-server-crud-data";
let data = {};

window.onload = function () {
    loadDataFromLocalStorage();

    let inputFieldsToStoreInLocalStorage = ["username", "password"];
    for (let elementId of inputFieldsToStoreInLocalStorage) {
        (function (elementId) {
            if (!data[elementId]) { data[elementId] = ""; }
            document.getElementById(elementId).value = data[elementId];
            document.getElementById(elementId).addEventListener("input", (e) => {
                data[elementId] = document.getElementById(elementId).value;
                saveDataToLocalStorage();
            });
        })(elementId);
    }

    showSchema();
};

function executeSQL () {
    let boxOutput = document.getElementById("box-output");
    let sqlBody = {
        referee: {
            name: document.getElementById("username").value,
            auth: document.getElementById("password").value,
        },
        sqlStatement: document.getElementById("sql-statement").value,
    };
    fetch("/api/v2/sql", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(sqlBody)
    })
    .then(response => response.json())
    .then(json => {
        boxOutput.innerHTML = "";
        let div, el, table, thead, tr;
        if (json.error) {
            div = document.createElement("div");

            if (json.statement) {
                el = document.createElement("h2");
                el.appendChild(document.createTextNode(json.statement));
                div.appendChild(el);
            }

            el = document.createElement("p");
            el.appendChild(document.createTextNode(json.error));
            el.style.color = "#f00";
            div.appendChild(el);

            boxOutput.appendChild(div);
            return;
        }
        for (let row of json) {
            div = document.createElement("div");
            div.style.overflowX = "auto";

            el = document.createElement("h2");
            el.appendChild(document.createTextNode(row.statement));
            div.appendChild(el);

            if (row.result.length === 0 && row.description.length === 0) {
                el = document.createElement("p");
                el.appendChild(document.createTextNode("Successful"));
                div.appendChild(el);
            } else {
                table = document.createElement("table");
                thead = document.createElement("thead");
                thead.style.fontWeight = "bold";
                tr = document.createElement("tr");
                for (let columnTitle of row.description) {
                    el = document.createElement("td");
                    el.appendChild(document.createTextNode(columnTitle));
                    tr.appendChild(el);
                }
                thead.appendChild(tr);
                table.appendChild(thead);

                for (let resultRow of row.result) {
                    tr = document.createElement("tr");
                    for (let resultCell of resultRow) {
                        el = document.createElement("td");
                        el.appendChild(document.createTextNode(resultCell));
                        tr.appendChild(el);
                    }
                    table.appendChild(tr);
                }
                div.appendChild(table);
            }
            boxOutput.appendChild(div);
        }
    })
    .catch(error => {
        console.log(error);
        boxOutput.innerText = "Error: " + error;
    });
};

function showSchema () {
    let boxOutput = document.getElementById("schema");
    let sqlBody = {
        referee: {
            name: document.getElementById("username").value,
            auth: document.getElementById("password").value,
        },
        sqlStatement: "schema",
    };
    fetch("/api/v2/sql", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(sqlBody)
    })
    .then(response => response.json())
    .then(json => {
        boxOutput.innerHTML = "";
        let p, span, txt;
        for (let table of json[0].result) {
            p = document.createElement("p");

            for (let i=0; i<table.length; i++) {
                span = document.createElement("span");
                txt = table[i].split(" ")[0]
                txt+= (i === 0 ? ": " : (i !== table.length-1 ? ", " : ""));
                span.appendChild(document.createTextNode(txt));
                if (i === 0) { span.style.fontWeight = "bold"; }
                else { span.title = table[i].split(" ")[1]; }
                p.appendChild(span);
            }

            boxOutput.appendChild(p);
        }
    })
    .catch(error => {
        console.log(error);
        boxOutput.innerHTML = '<button type="button" onclick="showSchema()">Show Schema</button>';
    });
};

let saveDataToLocalStorage = function () {
    localStorage.setItem(LS_DATA, JSON.stringify(data));
};
let loadDataFromLocalStorage = function () {
    data = localStorage.getItem(LS_DATA);
	if (data === null) {
		data = {};
	} else {
		data = JSON.parse(data);
	}
};