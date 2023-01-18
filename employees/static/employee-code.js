function generate_employee_table(key, direction) {
    //
    // employees is a global variable defined in data\employees.js
    //
    let search_term = "";

    function get_search_term() {
        if (localStorage.getItem("search_term")) {
            return localStorage.getItem("search_term");
        } else {
            return "";
        }
    }

    function name_to_url(name) {
        let cp = name.indexOf(',');
        let last = name.substring(0, cp);
        let first = name.substring(cp + 2);
        let result = (first + last).toLowerCase().replace('.', '').replace(' ', '') + ".htm";
        return result;
    }

    function name_to_email(name) {
        let cp = name.indexOf(',');
        let last = name.substring(0, cp);
        let first_initial = name.substring(cp + 2, cp + 3);
        let result = (first_initial + last).toLowerCase().replace('.', '').replace(' ', '') + "@wwd.ca.gov";
        return result;
    }


    // determine if we should display the employee
    function display_employee(employee, search_text) {
        let dateOK = false;
        let today = new Date();
        let start_date = new Date(employee.start_date);
        let end_date = new Date(employee.end_date);
        if (start_date <= today && today <= end_date) {
            dateOK = true;
        }

        if (search_text == "") {
            return dateOK;
        }

        let alltext = employee.first_name +
                employee.last_name + employee.position + employee.phone +
                employee.email + employee.emp_id + employee.department;
        if (alltext.toLowerCase().indexOf(search_text.toLowerCase()) >= 0 && dateOK) {
            return true;
        } else {
            return false;
        }
    }

    function ascending_svg() {
        return '<svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-caret-up-fill" fill="currentColor" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M8 5.5L2.5 11h11L8 5.5z" clip-rule="evenodd"/></svg>';
    }

    function descending_svg() {
        return '<svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-caret-down-fill" fill="currentColor" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M8 10.5L13.5 5h-11L8 10.5z" clip-rule="evenodd"/></svg>';
    }

    // method to return sort svg
    function sort_svg(key) {
        if (localStorage.getItem("sort_by") == key) {
            if (localStorage.getItem("sort_direction") == "asc") {
                return ascending_svg();
            } else {
                return descending_svg();
            }
        } else {
            return "";
        }
    }

    // sort employees by key in direction
    function sort_employees(key, direction) {
        let dir = 1;
        if (direction == 'desc') {
            dir = -1;
        }
        if (key == 'emp_id') {
            cmp = 2;
        } else {
            cmp = 1;
        }

        employees.sort(function (a, b) {
            let akey = '';
            let bkey = '';

            if (key == 'name') {
                key = 'last_name';
            }

            if (cmp == 1) {
                akey = a[key];
                bkey = b[key];
            } else {
                akey = parseInt(a[key]);
                bkey = parseInt(b[key]);

                // zero pad akey and bkey
                akey = akey.toString().padStart(8, '0');
                bkey = bkey.toString().padStart(8, '0');
            }
            if (key == 'name') {
                akey = (a['last_name'] + a['first_name']).toLowerCase()
                bkey = (b['last_name'] + b['first_name']).toLowerCase()
            }

            if (akey < bkey) {
                return -1 * dir;
            }
            if (akey > bkey) {
                return 1 * dir;
            }
            return 0;
        });
    }

    function get_employee_image(employee) {
        function get_image_from_name(name) {
            let cp = name.indexOf(',');
            let last = name.substring(0, cp);
            let first = name.substring(cp + 2, cp + 3);
            let result = (first + last).toLowerCase().replace('.', '').replace(' ', '') + ".jpg";
            result = 'images/' + result;
            return result;
        }

        let result = "";
        if (employee.img == "") {
            result = get_image_from_name(employee.name);
        } else {
            result = employee.img;
        }
        return result;
    }

    search_term = get_search_term();
    sort_employees(key, direction);

    // generate table with employees data
    let s = "<table class='table table-striped table-info'>";
    // let s = "<table class='table table-striped table-bordered table-hover table-condensed'>";

    let name_sort = sort_svg("name");
    let dpt_sort = sort_svg("department");
    let position_sort = sort_svg("position");
    let phone_sort = sort_svg("phone");
    let id_sort = sort_svg("emp_id");
    let email_sort = sort_svg("email");

    // <div className="container text-left">
    //     <div className="row text-bg-primary">
    //         <div className="col">{{description}}</div>
    //         <div className="col">&nbsp;</div>
    //     </div>
    //     {% for f in files %}
    //     <div className="row">
    //         <div className="col">
    //             {% if f.islocal %}
    //             <a href="/{{ f.file }}" target="_blank">{{f.name}} - Download</a>
    //             {% else %}
    //             <a href="{{ f.url }}">{{f.name}}</a>
    //             {% endif %}
    //         </div>
    //     </div>
    //     {% endfor %}
    // </div>


    s += "<div class='container text-left'>";
    s += "<div class='row text-bg-primary'>";
    s += "<div class='col-md-2' onclick='click_sort(\"name\");'>Name" + name_sort + "</div>";
    s += "<div class='col-md-2' onclick='click_sort(\"email\")'>Email" + email_sort + "</div>";
    s += "<div class='col-md-2' onclick='click_sort(\"department\")'>Department" + dpt_sort + "</div>";
    s += "<div class='col-md-3' onclick='click_sort(\"position\")'>Position" + position_sort + "</div>";
    s += "<div class='col-md-2' onclick='click_sort(\"phone\");'>Phone" + phone_sort + "</div>";
    s += "<div class='col-md-1' onclick='click_sort(\"emp_id\");'>ID" + id_sort + "</div>";
    s += "</div>";
    //s += "<tbody>";
    for (var i = 0; i < employees.length; i++) {

        if (display_employee(employees[i], search_term)) {
            let details_url = "<a href='./";
            details_url += employees[i].emp_id;
            details_url += "' >" + employees[i].first_name + ' ' + employees[i].last_name + "</a>";
            let img_url = employees[i].image;

            s += "<div class='row' onmouseover='save_employee_id(" + employees[i].emp_id + ")' >";
            s += "<div class='col-md-2'><img src='" + img_url + "' width='30' />&nbsp;&nbsp;" + details_url + "</div>";
            s += "<div class='col-md-2'>" + employees[i].email + "</div>";
            s += "<div class='col-md-2'>" + employees[i].department + "</div>";
            s += "<div class='col-md-3'>" + employees[i].position + "</div>";
            s += "<div class='col-md-2'>" + employees[i].phone + "</div>";
            s += "<div class='col-md-1'>" + employees[i].emp_id + "</div>";
            s += "</div>"; // row
        }
    }
    s += "</div>"; // container
    let div_container = document.getElementById("employeestable");
    div_container.innerHTML = s;

    // update sortby and direction in dom object
    function update_sortby() {
        let sortby = document.getElementById("sortby");
        let txt = "Sort by: " + key + ", " + direction + " ";
        if (key != "name" || direction != "asc" || search_term != "") {
            txt += '<button onClick="reset_sort_search()">Reset Sort</button>'
        }
        txt += '<br>';
        sortby.innerHTML = txt;
    }

    // Not needed anymore.
    // update_sortby();

    // update search term in dom object
    function update_search_term() {
        let searchinputvalue = document.getElementById("searchvalue");
        let savedvalue = get_search_term();
        searchinputvalue.value = savedvalue;
    }

    update_search_term();

}

var sort_direction = "asc";
var sort_by = "name";

// get sort_by from localstorage if it exists
if (localStorage.getItem("sort_by")) {
    sort_by = localStorage.getItem("sort_by");
} else {
    localStorage.setItem("sort_by", sort_by);
}

// get sort_direction from localstorage if it exists
if (localStorage.getItem("sort_direction")) {
    sort_direction = localStorage.getItem("sort_direction");
} else {
    localStorage.setItem("sort_direction", sort_direction);
}

generate_employee_table(sort_by, sort_direction);

function click_sort(key) {
    if (localStorage.getItem("sort_by") == key) {
        // need to toggle sort direction
        if (localStorage.getItem("sort_direction") == "asc") {
            localStorage.setItem("sort_direction", "desc");
        } else {
            localStorage.setItem("sort_direction", "asc");
        }
    } else {
        localStorage.setItem("sort_by", key);
        localStorage.setItem("sort_direction", "asc");
    }
    generate_employee_table(localStorage.getItem("sort_by"), localStorage.getItem("sort_direction"));
}

function input_search() {
    let search = document.getElementById("searchvalue");
    search_term = search.value;
    localStorage.setItem("search_term", search_term);
    generate_employee_table(localStorage.getItem("sort_by"), localStorage.getItem("sort_direction"));
}

function reset_sort_search() {
    localStorage.setItem("sort_by", "name");
    localStorage.setItem("sort_direction", "asc");
    localStorage.setItem("search_term", "");
    generate_employee_table(localStorage.getItem("sort_by"), localStorage.getItem("sort_direction"));
}

function save_employee_id(id) {
    localStorage.setItem("employee_id", id);
}
