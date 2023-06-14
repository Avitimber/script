<!DOCTYPE html>
<html>

<head>
    <meta charset="UTF-8">
    <title>HOME</title>
    <style>
        table {
            width: 100%;
            border-collapse: collapse;
        }

        table thead tr {
            background-color: #008c8c;
            color: #fff;
        }

        table tbody tr:nth-child(odd) {
            background-color: #eee;
        }

        table tbody tr:hover {
            background-color: #ccc;
        }

        th,
        td {
            padding: 8px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }

        .pagination {
            display: inline-block;
        }

        .pagination a {
            color: black;
            float: left;
            padding: 8px 16px;
            text-decoration: none;
            border: 1px solid #ddd;
            margin: 0 4px;
        }

        .pagination a.active {
            background-color: #4CAF50;
            color: white;
            border: 1px solid #4CAF50;
        }

        .pagination a:hover:not(.active) {
            background-color: #ddd;
        }
    </style>
</head>

<body>
    <h2 style="text-align: center;">为您推荐</h2>

    <table id="myTable">
        <tr>
            <th>名称</th>
            <th>信息</th>
            <th>价格</th>
            <th>类型</th>
            <th>产地</th>
            <th>销量</th>
        </tr>
    </table>

    <div class="pagination" style="float: right;">
        <a href="#" id="firstPage">&laquo; 第一页</a>
        <a href="#" id="prevPage">&lsaquo; 上一页</a>
        <span id="currentPage"></span>/<span id="totalPages"></span>
        <a href="#" id="nextPage">下一页 &rsaquo;</a>
        <a href="#" id="lastPage">最后一页 &raquo;</a>
    </div>

    <script>
        var jsonData = {{ detail }}
        var data = JSON.parse(jsonData); // 应用程序传来的数据，以数组形式存储
        var currentPage = 1; // 当前页码
        var rowsPerPage = 10; // 每页显示的行数

        // 模拟从应用程序获取数据并更新data数组
        function fetchData() {
            // 这里假设应用程序传来一个包含所有数据的数组，并赋值给data变量
            // 示例数据，实际应根据应用程序的数据结构进行修改
            jsonData = {{ detail }};
            data = JSON.parse(jsonData)
            /* data = [
                ["数据1", "数据2", "数据3"],
                ["数据4", "数据5", "数据6"],
                ["数据4", "数据5", "数据6"],
                ["数据4", "数据5", "数据6"],
                ["数据4", "数据5", "数据6"],
                ["数据4", "数据5", "数据6"],
                ["数据4", "数据5", "数据6"],
                ["数据4", "数据5", "数据6"],
                ["数据4", "数据5", "数据6"],
                ["数据4", "数据5", "数据6"],
                ["数据4", "数据5", "数据6"],
                ["数据4", "数据5", "数据6"], 
                ["数据1", "数据2", "数据3", "数据4", "数据5", "数据6"],
                ["数据1", "数据2", "数据3", "数据4", "数据5", "数据6"],
                ["数据1", "数据2", "数据3", "数据4", "数据5", "数据6"],
                ["数据1", "数据2", "数据3", "数据4", "数据5", "数据6"],
                ["数据1", "数据2", "数据3", "数据4", "数据5", "数据6"],
                ["数据1", "数据2", "数据3", "数据4", "数据5", "数据6"],
                ["数据1", "数据2", "数据3", "数据4", "数据5", "数据6"],
                ["数据1", "数据2", "数据3", "数据4", "数据5", "数据6"],
                ["数据1", "数据2", "数据3", "数据4", "数据5", "数据6"],
                ["数据1", "数据2", "数据3", "数据4", "数据5", "数据6"],
                ["数据1", "数据2", "数据3", "数据4", "数据5", "数据6"],
                ["数据1", "数据2", "数据3", "数据4", "数据5", "数据6"],
                // 更多数据行...
            ]; */
        }

        // 根据当前页码和每页显示的行数，生成要显示的数据
        function generateTableData() {
            var startIndex = (currentPage - 1) * rowsPerPage;
            var endIndex = startIndex + rowsPerPage;
            return data.slice(startIndex, endIndex);
        }

        // 根据表格数据生成HTML并更新表格内容
        function updateTable() {
            var table = document.getElementById("myTable");
            var tableData = generateTableData();

            // 清空表格内容
            while (table.rows.length > 1) {
                table.deleteRow(1);
            }

            // 添加表格数据
            for (var i = 0; i < tableData.length; i++) {
                var row = table.insertRow();
                for (var j = 0; j < tableData[i].length; j++) {
                    var cell = row.insertCell();
                    cell.innerHTML = tableData[i][j];
                }
            }
        }
        // 更新分页信息
        function updatePagination() {
            var totalPages = Math.ceil(data.length / rowsPerPage);
            var currentPageElement = document.getElementById("currentPage");
            var totalPagesElement = document.getElementById("totalPages");

            currentPageElement.innerHTML = currentPage;
            totalPagesElement.innerHTML = totalPages;

            var firstPageLink = document.getElementById("firstPage");
            var prevPageLink = document.getElementById("prevPage");
            var nextPageLink = document.getElementById("nextPage");
            var lastPageLink = document.getElementById("lastPage");

            // 根据当前页码设置分页链接的状态
            if (currentPage === 1) {
                firstPageLink.classList.add("disabled");
                prevPageLink.classList.add("disabled");
            } else {
                firstPageLink.classList.remove("disabled");
                prevPageLink.classList.remove("disabled");
            }

            if (currentPage === totalPages) {
                nextPageLink.classList.add("disabled");
                lastPageLink.classList.add("disabled");
            } else {
                nextPageLink.classList.remove("disabled");
                lastPageLink.classList.remove("disabled");
            }
        }

        // 切换到指定页码的数据并更新表格和分页信息
        function goToPage(pageNum) {
            currentPage = pageNum;
            updateTable();
            updatePagination();
        }

        // 第一页链接点击事件
        document.getElementById("firstPage").addEventListener("click", function (event) {
            event.preventDefault();
            if (currentPage !== 1) {
                goToPage(1);
            }
        });

        // 上一页链接点击事件
        document.getElementById("prevPage").addEventListener("click", function (event) {
            event.preventDefault();
            if (currentPage > 1) {
                goToPage(currentPage - 1);
            }
        });

        // 下一页链接点击事件
        document.getElementById("nextPage").addEventListener("click", function (event) {
            event.preventDefault();
            var totalPages = Math.ceil(data.length / rowsPerPage);
            if (currentPage < totalPages) {
                goToPage(currentPage + 1);
            }
        });

        // 最后一页链接点击事件
        document.getElementById("lastPage").addEventListener("click", function (event) {
            event.preventDefault();
            var totalPages = Math.ceil(data.length / rowsPerPage);
            if (currentPage !== totalPages) {
                goToPage(totalPages);
            }
        });

        // 初始化页面
        fetchData();
        updateTable();
        updatePagination();
    </script>
</body>

</html>
