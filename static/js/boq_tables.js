let tableTargetDiv;
let divOrder;
let key, table_pk, totalPk;


function getTable(type){
    const tables = {
        "Floor":`<div id="${key}_div" class="d-flex flex-column row-gap-2 bg-white rounded-4 p-4 shadow-sm">
        <div class="d-flex flex-column row-gap-3 overflow-auto">
                <div class="d-flex justify-content-between align-items-center mt-3">
                    <div class="">
                        <div class="input-group">
                            <span class="input-group-text" id="basic-addon1">Table Name</span>
                            <input type="text" class="form-control table-name" name="table-heading-name"  data-model="Floor" data-value="${key}"  value="${key}">
                        </div>
                    </div>
                    <div class="d-flex justify-content-end">
                        <div class="d-flex column-gap-3">
                            <button data-main-table="${key}" data-secondary-table="gst_${key}"  class="fw-medium c_btn fs-6 bg-white border border-2 rounded-3 d-flex align-items-center column-gap-2 p-2">
                                <span class="material-symbols-rounded fs-4">collapse_all</span>
                                <span>Collapse Table</span>
                            </button>
                            <button data-id="gst_${key}" class="fw-medium gst_btn fs-6 bg-white border border-2 rounded-3 d-flex align-items-center column-gap-2 p-2">
                                <span class="material-symbols-rounded fs-4">collapse_all</span>
                                <span>GST ON/OFF</span>
                            </button>
                        </div>
                    </div>
                </div>
                <div class="d-flex column-gap-2 overflow-auto">
                    <table class="table table-bordered col-9" id="${key}">
                        <thead>
                            <tr class="fw-medium text-center">
                                <th>A</th>
                                <th></th>
                                <th>CODE</th>
                                <th>WORK DETAIL</th>
                                <th>N(N)</th>
                                <th>L(M)</th>
                                <th>W(M2)</th>
                                <th>H(M3)</th>
                                <th>QUANTITY</th>
                                <th>UNITS</th>
                                <th>RATE PER UNIT</th>
                                <th>FULL AMOUNT</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr class="table-row">
                                <td>
                                    <div class="table-row-buttons d-none column-gap-3">
                                        <button data-table-type="floor" class="add-row-btn ar_btn btn d-flex bg-white border border-2 rounded-3 d-flex align-items-center column-gap-2 p-2">
                                            <span class="material-symbols-rounded fs-4">add</span>
                                            <span>Add Row</span>
                                        </button>
                                        <button data-pk="${table_pk}" data-table-type="Floor" class="del-row-btn btn d-flex  bg-white border border-2 rounded-3 d-flex align-items-center column-gap-2 p-2">
                                            <span class="material-symbols-rounded fs-4">delete</span>
                                            <span>Delete Row</span>
                                        </button>
                                    </div>
                                </td>
                                <input type="hidden" id="csrf_token" name="csrfmiddlewaretoken" value="${getCookie("csrftoken")}" />
                                <input type="hidden" class="pk_row" name="pk_row_floor" id="pk_Floor_${table_pk}" value="${table_pk}" />
                                <td class="bg-white" rowspan="1">
                                    <textarea name="multiline_form_description" rowspan="1" class="form-control" data-model="Floor" data-field="description"></textarea>
                                </td>
                                <td>
                                    <select name="multiline_form_code" data-model="Floor" data-field="code" id="multiline_form_code_${table_pk}" class="form-select">
                                        <option selected disabled>Select Code</option>
                                    </select>
                                </td>
                                <td><input type="text" name="multiline_form_workdetail" id="multiline_form_workdetail_${table_pk}" placeholder="Work Detail" data-model="Floor" data-field="work_detail" class="form-control" value="" /></td>
                                <td><input type="text" name="multiline_form_N" id="multiline_form_N_${table_pk}" class="form-control" data-model="Floor" data-field="N" value="" /></td>
                                <td><input type="text" name="multiline_form_L" id="multiline_form_L_${table_pk}" class="form-control" data-model="Floor" data-field="L" value="" /></td>
                                <td><input type="text" name="multiline_form_W" id="multiline_form_W_${table_pk}" class="form-control" data-model="Floor" data-field="W" value="" /></td>
                                <td><input type="text" name="multiline_form_H" id="multiline_form_H_${table_pk}" class="form-control" data-model="Floor" data-field="H" value="" /></td>
                                <td><input type="text" name="multiline_form_quantity" id="multiline_form_quantity_${table_pk}" disabled class="form-control" data-model="Floor" data-field="quantity" value="" /></td>
                                <td>
                                    <select name="multiline_form_unit" class="form-select" data-model="Floor" data-field="unit" required>
                                    </select>
                                </td>
                                <td><input type="text" name="multiline_form_rateperunit" id="multiline_form_rateperunit_${table_pk}" disabled data-model="Floor" data-field="rate_per_unit" class="form-control" value="" /></td>
                                <td><input type="text" name="multiline_form_fullamount" id="multiline_form_fullamount_${table_pk}" disabled data-model="Floor" data-field="full_amount" class="form-control " value="" /></td>
                            </tr>
                        </tbody>
                        <tbody>
                            <tr class="table-row1 bg-primary-subtle" id="totalcolum-multiline">
                                <input type="hidden" name="total_pk" value="">
                                <td class="disabled " colspan="11">Total</td>
                                <td>
                                    <input type="text" class="form-control bg-primary-subtle total-amount" disabled value="" />
                                </td>
                            </tr>
                        </tbody>
                    </table>
                    <table class="table table-bordered" id="gst_${key}">
                        <thead>
                            <tr>
                                <th>BASIC AMOUNT</th>
                                <th>GST APPLIED</th>
                                <th>GST AMOUNT</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr class="table-row disabled">
                                <input type="hidden" class="pk_row" name="pk_row_floor" id="pk_Floor_${table_pk}" value="${table_pk}" />
                                <td><input type="text" name="mf_totalbasicamount" disabled data-model="Floor" data-field="basic_amount" id="mf_totalbasicamount_${table_pk}" class="form-control" value="" /></td>
                                <td><input type="text" name="mf_gst" disabled id="mf_gst_${table_pk}" class="form-control" data-model="Floor" data-field="gst_applied" value="" /></td>
                                <td><input type="text" name="mf_gstamount" disabled id="mf_gstamount_${table_pk}" data-model="Floor" data-field="gst_amount" class="form-control" value="" /></td>
                            </tr>
                        </tbody>
                        <tbody>
                            <tr class="bg-primary-subtle">
                                <input type="hidden" name="mainTable" value="${key}">
                                <input type="hidden" name="total_pk" value="${totalPk}">
                                <td><input type="text" disabled class="form-control bg-primary-subtle total-basic-amount" value=""></td>
                                <td><input type="text" disabled class="form-control bg-primary-subtle total-gst" value=""></td>
                                <td><input type="text" disabled class="form-control bg-primary-subtle total-gst-amount" value=""></td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                <div class="d-flex column-gap-3 mt-3">
                    <button data-id="${key}" class="fw-medium dp_btn fs-6 bg-white border border-2 rounded-3 d-flex align-items-center column-gap-2 p-2">
                        <span class="material-symbols-rounded fs-4">tab_duplicate</span>
                        <span>Duplicate Table</span>
                    </button>
                </div>
        </div>
    </div>
    <div class="d-flex column-gap-2 align-items-center">
        <div class="border-bottom w-100 flex-1"></div>
        <button type="button" data-id="${key}_div"  class="btn btn-primary col-1" data-bs-toggle="modal" data-bs-target="#addTable">Add Table</button>
        <div class="border-bottom w-100 flex-1"></div>
    </div>
    `,
        "WallMasonry":`<div id="${table_pk}_div" class="d-flex flex-column row-gap-2 bg-white rounded-4 p-4 shadow-sm">
        <div class="d-flex justify-content-between align-items-center mt-3">
            <div class="">
                <div class="input-group">
                    <span class="input-group-text" id="basic-addon1">Table Name</span>
                    <input type="text" class="form-control table-name" name="table-heading-name" data-model="WallMasonry" data-value="${table_pk}" value="${table_pk}" />
                </div>
            </div>
            <div class="d-flex justify-content-end">
                <div class="d-flex column-gap-3">
                    <button data-main-table="${table_pk}" data-secondary-table="gst_${table_pk}"  class="fw-medium c_btn fs-6 bg-white border border-2 rounded-3 d-flex align-items-center column-gap-2 p-2">
                        <span class="material-symbols-rounded fs-4">collapse_all</span>
                        <span>Collapse Table</span>
                    </button>
                    <button data-id="gst_${table_pk}" class="fw-medium gst_btn fs-6 bg-white border border-2 rounded-3 d-flex align-items-center column-gap-2 p-2">
                        <span class="material-symbols-rounded fs-4">collapse_all</span>
                        <span>GST ON/OFF</span>
                    </button>
                </div>
            </div>
        </div>
        <div class="d-flex column-gap-2 overflow-auto">
            <table class="table table-bordered col-9" id="${table_pk}">
                <thead>
                    <tr class="fw-medium text-center">
                        <th>B</th>
                        <th></th>
                        <th>CODE</th>
                        <th>WORK DETAIL</th>
                        <th>N(N)</th>
                        <th>L(M)</th>
                        <th>W(M2)</th>
                        <th>H(M3)</th>
                        <th>QUANTITY</th>
                        <th>UNITS</th>
                        <th>FULL RATE</th>
                        <th>FULL AMOUNT</th>
                    </tr>
                </thead>
                <tbody>
                    <tr class="table-row">
                        <td>
                            <div class="table-row-buttons d-none column-gap-3">
                                <button data-table-type="wall" class="add-row-btn btn d-flex bg-white border border-2 rounded-3 d-flex align-items-center column-gap-2 p-2">
                                    <span class="material-symbols-rounded fs-4">add</span>
                                    <span>Add Row</span>
                                </button>
                                <button data-pk="${table_pk}" data-table-type="Wall" class="del-row-btn btn d-flex  bg-white border border-2 rounded-3 d-flex align-items-center column-gap-2 p-2">
                                    <span class="material-symbols-rounded fs-4">delete</span>
                                    <span>Delete Row</span>
                                </button>
                            </div>
                        </td>
                        <input type="hidden" id="csrf_token" name="csrfmiddlewaretoken" value="${getCookie("csrftoken")}" />
                        <input type="hidden" class="pk_row" name="pk_row_wall" id="pk_Wall_${table_pk}" value="${table_pk}" />
                        <td class="bg-white" rowspan="1">
                            <textarea name="multiline_form_description" rowspan="1" class="form-control" data-model="WallMasonry" data-field="description"></textarea>
                        </td>
                        <td class="code-td" rowspan="1"></td>
                        <td>
                            <input type="text" name="multiline_form_workdetail" data-model="WallMasonry" data-field="work_detail" value="" id="multiline_form_workdetail_${table_pk}" class="form-control" />
                        </td>
                        <td><input type="text" name="multiline_form_N" data-model="WallMasonry" data-field="N" id="multiline_form_N_${table_pk}" value="" class="form-control" /></td>
                        <td><input type="text" name="multiline_form_L" data-model="WallMasonry" data-field="L" id="multiline_form_L_${table_pk}" value="" class="form-control" /></td>
                        <td><input type="text" name="multiline_form_W" id="multiline_form_W_${table_pk}" data-model="WallMasonry" data-field="W" value="" class="form-control" /></td>
                        <td><input type="text" name="multiline_form_H" data-model="WallMasonry" data-field="H" id="multiline_form_H_${table_pk}" value="" class="form-control" /></td>
                        <td>
                            <input type="text" name="multiline_form_quantity" data-model="WallMasonry" data-field="quantity" value="" disabled id="multiline_form_quantity_${table_pk}" class="form-control" />
                        </td>
                            <td class="unit-td" rowspan="1"></td>
                            <td class="rate-td" rowspan="1"></td>
                            <td class="amount-td" rowspan="1"></td>
                    </tr>
                </tbody>
                <tbody>
                    <tr class="table-row disabled bg-primary-subtle">
                        <input type="hidden" name="total_pk" value="${totalPk}" />
                        <td colspan="2"></td>
                        <td>
                            <select name="multiline_form_code" data-model="WallMasonry" data-field="code" id="multiline_form_code_" class="form-select wall bg-primary-subtle">
                                <option selected disabled>Select Code</option>
                            </select>
                        </td>
                        <td colspan="5"></td>
                        <td><input type="text" class="form-control bg-primary-subtle total-quantity" disabled value="" /></td>
                        <td><input type="text" class="form-control bg-primary-subtle total-unit" disabled value="" /></td>
                        <td><input type="text" name="multiline_form_rateperunit" disabled class="form-control bg-primary-subtle total-full-rate" value="" /></td>
                        <td><input type="text" class="form-control bg-primary-subtle wall total-amount" value="" readonly /></td>
                    </tr>
                </tbody>
            </table>
            <table class="table table-bordered td-borderless" id="gst_${table_pk}">
                <thead>
                    <tr>
                        <th>BASIC AMOUNT</th>
                        <th>GST APPLIED</th>
                        <th>GST AMOUNT</th>
                    </tr>
                </thead>
                <tbody>
                    <tr class="disabled">
                        <td></td>
                        <td></td>
                        <td></td>
                    </tr>
                </tbody>
                <tbody>
                    <tr class="bg-primary-subtle">
                        <input type="hidden" name="mainTable" value="${table_pk}" />
                        <input type="hidden" name="total_pk" value="${totalPk}" />
                        <td><input type="text" disabled value="" class="form-control bg-primary-subtle total-basic-amount" /></td>
                        <td><input type="text" disabled value="" class="form-control bg-primary-subtle total-gst" /></td>
                        <td><input type="text" disabled value=""class="form-control bg-primary-subtle total-gst-amount" /></td>
                    </tr>
                </tbody>
            </table>
        </div>
        <div class="d-flex column-gap-3">
            <button data-id="${table_pk}" class="fw-medium dp_btn fs-6 bg-white border border-2 rounded-3 d-flex align-items-center column-gap-2 p-2">
                <span class="material-symbols-rounded fs-4">tab_duplicate</span>
                <span>Duplicate Table</span>
            </button>
        </div>
    </div>
    <div class="d-flex column-gap-2 align-items-center">
        <div class="border-bottom w-100 flex-1"></div>
        <button type="button" data-id="${table_pk}_div" class="btn btn-primary col-1" data-bs-toggle="modal" data-bs-target="#addTable">Add Table</button>
        <div class="border-bottom w-100 flex-1"></div>
    </div>`,
        "Finishing":`<div id="${table_pk}_div" class="d-flex flex-column row-gap-2 bg-white rounded-4 p-4 shadow-sm">
            <div class="d-flex justify-content-between align-items-center mt-3">
                <div class="">
                    <div class="input-group">
                        <span class="input-group-text" id="basic-addon1">Table Name</span>
                        <input type="text" class="form-control table-name" name="table-heading-name" data-model="Finishing" data-value="${table_pk}" value="${table_pk}" />
                    </div>
                </div>
                <div class="d-flex justify-content-end">
                    <div class="d-flex column-gap-3">
                        <button data-main-table="${table_pk}" data-secondary-table="gst_${table_pk}"  class="fw-medium c_btn fs-6 bg-white border border-2 rounded-3 d-flex align-items-center column-gap-2 p-2">
                            <span class="material-symbols-rounded fs-4">collapse_all</span>
                            <span>Collapse Table</span>
                        </button>
                        <button data-id="gst_${table_pk}" class="fw-medium gst_btn fs-6 bg-white border border-2 rounded-3 d-flex align-items-center column-gap-2 p-2">
                            <span class="material-symbols-rounded fs-4">collapse_all</span>
                            <span>GST ON/OFF</span>
                        </button>
                    </div>
                </div>
            </div>
            <div class="d-flex column-gap-2 overflow-auto">
                <table class="table table-bordered col-9 table-c" id="${table_pk}">
                    <thead>
                        <tr class="fw-medium text-center">
                            <th>C</th>
                            <th></th>
                            <th>FREE CODE</th>
                            <th>WORK DETAIL</th>
                            <th>ADD BASIC PRICE</th>
                            <th>ADD GST</th>
                            <th>QUANTITY</th>
                            <th>UNITS</th>
                            <th>FULL RATE</th>
                            <th>FULL AMOUNT</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr class="table-row">
                            <input type="hidden" id="csrf_token" name="csrfmiddlewaretoken" value="${getCookie("csrftoken")}" />
                            <input type="hidden" class="pk_row" name="pk_row_product" id="pk_ Finishing" value="${table_pk}" />
                            <td>
                                <div class="table-row-buttons d-none column-gap-3">
                                    <button data-table-type="finishing" class="add-row-btn btn d-flex bg-white border border-2 rounded-3 d-flex align-items-center column-gap-2 p-2">
                                        <span class="material-symbols-rounded fs-4">add</span>
                                        <span>Add Row</span>
                                    </button>
                                    <button data-pk="${table_pk}" data-table-type="Finishing" class="del-row-btn btn d-flex  bg-white border border-2 rounded-3 d-flex align-items-center column-gap-2 p-2">
                                        <span class="material-symbols-rounded fs-4">delete</span>
                                        <span>Delete Row</span>
                                    </button>
                                </div>
                            </td>
                                <td class="bg-white" rowspan="1"><textarea name="basic_form_description" data-model="Finishing" data-field="description" class="form-control"></textarea>
                            </td>
                            <td><input type="text" name="basicform_code" id="basicform_code_${table_pk}" data-model="Finishing" data-field="free_code" value="" class="form-control" /></td>
                            <td><textarea name="basicform_workdetails" class="form-control" data-model="Finishing" data-field="work_detail"></textarea></td>
                            <td><input type="text" name="basicform_basicrate" id="basicform_basicrate_${table_pk}" data-model="Finishing" data-field="basic_rate" value="" class="form-control" /></td>
                            <td>
                                <select name="basicform_gst" id="basicform_gst_${table_pk}" class="form-select" data-model="Finishing" data-field="gst" value="" required>
                                    <option value="" disabled selected>Select</option>
                                </select>
                            </td>
                            <td><input type="text" name="basicform_quantity" id="basicform_quantity_${table_pk}" data-model="Finishing" data-field="quantity" value="" class="form-control" /></td>
                            <td>
                                <select name="basicform_unit" class="form-select" id="basicform_unit_${table_pk}" data-model="Finishing" data-field="unit" value="" required>
                                    <option value="" disabled selected>Select</option>
                                </select>
                            </td>
                            <td><input type="text" name="basicform_fullrate" id="basicform_fullrate_${table_pk}" data-model="Finishing" data-field="full_rate" disabled value="" class="form-control" /></td>
                            <td><input type="text" name="basicform_fullamount" id="basicform_fullamount_${table_pk}" class="form-control" data-model="Finishing" disabled data-field="full_amount" value="" /></td>
                        </tr>
                    </tbody>
                    <tbody>
                        <tr class="table-row1 bg-primary-subtle disabled" id="totalcolum-finishing">
                            <td class="disabled" colspan="9">Total</td>
                            <td>
                                <input type="text" class="form-control bg-primary-subtle total-amount" disabled value="" readonly />
                            </td>
                        </tr>
                    </tbody>
                </table>
                <table class="table table-bordered" id="gst_${table_pk}">
                    <thead>
                        <tr>
                            <th>BASIC AMOUNT</th>
                            <th>GST APPLIED</th>
                            <th>GST AMOUNT</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr class="disabled">
                            <td><input type="text" name="bf_totalbasicamount" disabled id="bf_totalbasicamount_${table_pk}" data-model="Finishing" data-field="basic_amount" value="" class="form-control" /></td>
                            <td>
                                <input name="bf_gst" id="bf_gst_${table_pk}" disabled  data-model="Finishing" class="form-control" data-field="gst_applied" value="" />
                            </td>
                            <td><input type="text" name="bf_gstamount" disabled  id="bf_gstamount_${table_pk}" data-model="Finishing" data-field="gst_amount" value="" class="form-control" /></td>
                        </tr>
                    </tbody>
                    <tbody>
                        <tr class="bg-primary-subtle">
                            <input type="hidden" name="mainTable" value="${table_pk}">
                            <td><input type="text" disabled class="form-control bg-primary-subtle total-basic-amount" /></td>
                            <td><input type="text" disabled class="form-control bg-primary-subtle total-gst" /></td>
                            <td><input type="text" disabled class="form-control bg-primary-subtle total-gst-amount" /></td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <div class="d-flex column-gap-3">
                <button data-id="${table_pk}" class="fw-medium dp_btn fs-6 bg-white border border-2 rounded-3 d-flex align-items-center column-gap-2 p-2">
                    <span class="material-symbols-rounded fs-4">tab_duplicate</span>
                    <span>Duplicate Table</span>
                </button>
            </div>
    </div>
    <div class="d-flex column-gap-2 align-items-center">
        <div class="border-bottom w-100 flex-1"></div>
        <button type="button" data-id="${table_pk}_div" class="btn btn-primary col-1" data-bs-toggle="modal" data-bs-target="#addTable">Add Table</button>
        <div class="border-bottom w-100 flex-1"></div>
    </div>
    `
    }

    return tables[type]
}

function requestNewTable(type, order) {
    return new Promise((resolve, reject) => {
        $.ajax({
            url: `/client/boq/${projectPK}/create-table/`,
            type: "POST",
            contentType: "application/json",
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
            },
            data: JSON.stringify({
                type: type,
                order: order
            }),
            success: function (response) {
                resolve(response);
            },
            error: function (error) {
                reject(error);
            }
        });
    });
}


function addTable(type) {
    requestNewTable(type, divOrder)
        .then(table_data => {
            console.log("Table Data:", table_data);  // Log the entire response

            key = table_data["key"];
            totalPk = table_data["total_pk"];
            console.log("Key:", key, "Total PK:", totalPk);  // Check if keys are defined

            let table = getTable(type);
            console.log("Table HTML:", table);  // Check the generated HTML

            // Ensure tableTargetDiv is a valid element before appending
            if (tableTargetDiv) {
                tableTargetDiv.insertAdjacentHTML('afterend', table);

                table = document.getElementById(key);
                if (table) {
                    console.log("Inserted Table Element:", table);  // Verify the element is created

                    let codeSelect = table.querySelector("select[name='multiline_form_code']");
                    if (codeSelect) {
                        for (const [key, value] of Object.entries(codeValues)) {
                            const option = document.createElement('option');
                            option.value = key;
                            option.textContent = value;
                            codeSelect.appendChild(option);
                        }
                    }

                    let unitSelect = table.querySelector("select[name='multiline_form_unit']");
                    if (unitSelect) {
                        for (const [key, value] of Object.entries(unitValues)) {
                            const option = document.createElement('option');
                            option.value = key;
                            option.textContent = value;
                            unitSelect.appendChild(option);
                        }
                    }

                    let gstSelect = table.querySelector("select[name='basicform_gst']");
                    if (gstSelect) {
                        for (const [key, value] of Object.entries(gstValues)) {
                            const option = document.createElement('option');
                            option.value = key;
                            option.textContent = value;
                            gstSelect.appendChild(option);
                        }
                    }
                } else {
                    console.error("Table element not found for key:", key);
                }
            } else {
                console.error("tableTargetDiv is not defined.");
            }

             location.reload()
//             location.reload();
        })
        .catch(error => {
            console.error("Error creating table:", error);
        });
}


document.addEventListener("DOMContentLoaded", function () {
    const addTableBtns = document.querySelectorAll("button[data-bs-target='#addTable']")
    addTableBtns.forEach((element) => {
        element.addEventListener("click", function () {
            tableTargetDiv = element.closest("div");
            divOrder = element.getAttribute("data-order")
        });
    });
});
