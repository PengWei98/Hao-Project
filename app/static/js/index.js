function upload_file() {
    var form = document.forms.namedItem("upload_form");
    var fd = new FormData(form);

    $.ajax({
            url: "/upload",
            type: "POST",
            data: fd,
            async: true,
            cashe: false,
            contentType: false,
            processData: false,
            beforeSend: function () {
                $('#loadingModal').modal({backdrop: 'static', keyboard: false});
            },
            success: function (table_data) {
                $('#loadingModal').modal('hide');
                if (table_data.table.length == 0) {
                    alert("Sorry! We don't find any table in the paper!");
                    return;
                }
                document.getElementsByTagName('body')[0].classList.add("modal-open");
                $("#tableModal").modal("show");
                for (i in table_data.table) {
                    var tr;
                    tr = "<tr>"
                    for (j in table_data.table[i]) {
                        tr = tr + '<td>' + table_data.table[i][j] + '</td>'
                    }
                    tr = tr + "</tr>"
                    $("#pdf_table").append(tr)
                }
                var parent = document.getElementById("pdf_table");
                var div = document.createElement("div");
                div.setAttribute("id", "table_id");
                div.setAttribute("hidden", "")
                div.innerHTML = table_data.id;
                parent.appendChild(div);

            },
            error: function (table_data) {
                $('#loadingModal').modal('hide');
                alert("Fail to Upload!");
            },
            complete: function () {
                $('#loadingModal').modal('hide');
            }

        }
    )
}

function correct_pdf_table() {
    var id = document.getElementById("table_id").innerText;
    window.location.href = "/db_table?id=" + id;
}

function incorrect_pdf_table() {
    window.location.href = "/index?state=1";
}

function submit_remark() {
    $.ajax({
        url: "/remark",
        type: "POST",
        data: $('#remark_form').serialize(),
        async: false,
        error: function (request) {
            alert("Connection error");
        },
        success: function (data) {
            $('#remarkModal').modal({
                backdrop: true,
                keyboard: true,
                show: true
            });
            setTimeout(function () {
                $("#remarkModal").modal("hide")
            }, 3000);
        }
    })
}

function search_1() {
    var value = document.getElementById("search1").value;
    $.ajax({
        url: "/search1?text=" + value,
        type: "GET",
        async: false,
        error: function (request) {
            alert("Connection error");
        },
        success: function (table_data) {
            if (table_data.methods.length == 0) {
                $("#noResultModal").modal("show");
            } else {
                $("#searchingModal").modal("show");
                var tr = '';
                for (i in table_data.methods) {
                    tr = tr + '<tr><td class="text-center">' + table_data.methods[i] + '</td></tr>';
                }
                $("#searching_table").append(tr);
                var parent = document.getElementById("searching_tr");
                var div = document.createElement("th");
                div.setAttribute("class", "text-center");
                div.innerHTML = "Methods";
                parent.appendChild(div);
            }
        }
    })
}

function search_2() {
    var value = document.getElementById("search2").value;
    $.ajax({
        url: "/search2?text=" + value,
        type: "GET",
        async: false,
        error: function (request) {
            alert("Connection error");
        },
        success: function (table_data) {
            if (table_data.metrics.length == 0) {
                $("#noResultModal").modal("show");
            } else {
                $("#searchingModal").modal("show");
                var tr = '';

                for (i in table_data.metrics) {
                    tr = tr + '<tr><td class="text-center">' + table_data.metrics[i] + '</td></tr>';
                }
                $("#searching_table").append(tr);
                var parent = document.getElementById("searching_tr");
                var div = document.createElement("th");
                div.setAttribute("class", "text-center");
                div.innerHTML = "Metrics";
                parent.appendChild(div);
            }
        }
    })
}

function search_3() {
    var value = document.getElementById("search3").value;
    $.ajax({
        url: "/search3?text=" + value,
        type: "GET",
        async: false,
        error: function (request) {
            alert("Connection error");
        },
        success: function (table_data) {
            if (table_data.datasets.length == 0) {
                $("#noResultModal").modal("show");
            } else {
                $("#searchingModal").modal("show");
                var tr = '';
                for (i in table_data.datasets) {
                    tr = tr + '<tr><td class="text-center">' + table_data.datasets[i] + '</td></tr>';
                }
                $("#searching_table").append(tr);
                var parent = document.getElementById("searching_tr");
                var div = document.createElement("th");
                div.setAttribute("class", "text-center");
                div.innerHTML = "Datasets";
                parent.appendChild(div);
            }
        }
    })
}

