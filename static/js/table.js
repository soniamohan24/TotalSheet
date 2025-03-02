const projectPK = document.getElementById("pk").textContent;
// ====================
// Utility Functions
// ====================
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === name + "=") {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function updateElementIDs(element) {
    const elementsWithID = element.querySelectorAll("[id]");
    elementsWithID.forEach((el) => {
        el.id = `${el.id}_${new Date().getTime()}`;
    });
}

function getNthParent(elem, n) {
    return n === 0 ? elem : getNthParent(elem.parentNode, n - 1);
}

function getGSTRowByElement(element) {
    let currentRow = element.closest("tr");
    let rowIndex = Array.from(currentRow.parentNode.children).indexOf(currentRow);
    let gstTable = element.closest("table").nextElementSibling;
    let gstRow = gstTable.querySelectorAll("tr")[rowIndex + 1];
    return gstRow;
}

function getGSTTableByRow(row) {
    let gstTable = row.closest("table").nextElementSibling;

    return gstTable;
}

function getFieldValuesFromRow(row){
    const fieldValues = {};
    let fields = row.querySelectorAll('input:not([type="hidden"]), textarea, select');
    fields.forEach((field) => {
        const key = field.getAttribute("data-field");
        const value = field.value;
        if (key) {
            fieldValues[key] = value === "" ? null : value;
        }
    });
    return fieldValues
}

// Function to update quantity
function updateQuantity(row) {
    const multiline_l = row.querySelector('input[name="multiline_form_L"]');
    const multiline_n = row.querySelector('input[name="multiline_form_N"]');
    const multiline_w = row.querySelector('input[name="multiline_form_W"]');
    const multiline_h = row.querySelector('input[name="multiline_form_H"]');
    const multiline_form_quantity = row.querySelector('input[name="multiline_form_quantity"]');
    const multiline_form_fullamount = row.querySelector('input[name="multiline_form_fullamount"]');
    const multiline_form_basicamount = row.querySelector('input[name="mf_totalbasicamount"]');
    const mf_gst = row.querySelector('input[name="mf_gst"]');
    const gst_amount = row.querySelector('input[name="gst_amount"]');


    rateperunitField = row.querySelector('input[name="multiline_form_rateperunit"]');

    //let gstRow = getGSTRowByElement(rateperunitField)
    //let totalBasicAmount = gstRow.querySelector('input[name="mf_totalbasicamount"]');
    //totalBasicAmountField = gstRow.querySelector('input[name="mf_totalbasicamount"]');

    const l = parseFloat(multiline_l.value) || 1;
    const n = parseFloat(multiline_n.value) || 1;
    const w = parseFloat(multiline_w.value) || 1;
    const h = parseFloat(multiline_h.value) || 1;

    const quantity = l * n * w * h;
    if (multiline_l.value == 0 && multiline_n.value == 0 && multiline_w.value == 0 && multiline_h.value == 0){
        multiline_form_quantity.value = 0;
    }else{
        multiline_form_quantity.value = quantity.toFixed(2);
    }

    if (rateperunitField) {
        const rate_per_unit = parseFloat(rateperunitField.value);
        //const BasicAmount = parseFloat( totalBasicAmountField.value);
        const event = new Event("change");
         //const event1 = new Event("change");
        rateperunitField.dispatchEvent(event);
        //totalBasicAmountField.dispatchEvent(event1);
        //totalBasicAmount.dispatchEvent(event);
        //const originalBasicAmount = parseFloat(totalBasicAmountField.dataset.originalBasicAmount) || 0;
        multiline_form_fullamount.value = (multiline_form_quantity.value * rate_per_unit).toFixed(2);
       // totalBasicAmount.value=(multiline_form_quantity.value * BasicAmount).toFixed(2);

    }

   //updateUnit(multiline_l, multiline_n, multiline_w, multiline_h, row);
}

// Function to update the unit based on which fields have values
function updateUnit(multiline_l, multiline_n, multiline_w, multiline_h, row) {
    const hasL = parseFloat(multiline_l.value) > 0;
    const hasN = parseFloat(multiline_n.value) > 0;
    const hasW = parseFloat(multiline_w.value) > 0;
    const hasH = parseFloat(multiline_h.value) > 0;

    let logicalUnit = "";
    let count = 0;

    if (hasL) count++;
    if (hasN) count++;
    if (hasW) count++;
    if (hasH) count++;

    if (count === 1) {
        logicalUnit = "N";
    } else if (count === 2) {
        logicalUnit = "M";
    } else if (count === 3) {
        logicalUnit = "M2";
    } else if (count === 4) {
        logicalUnit = "M3";
    }

    const unitSelect = row.querySelector('select[name="multiline_form_unit"]');

    if (unitSelect && count != 0) {
        const options = Array.from(unitSelect.options);
        const unitOption = options.find((option) => option.text === logicalUnit);
        unitSelect.value = unitOption.value;
    }

    calculateTotal();
    const lastRow = getNthParent(row, 2).querySelectorAll("tbody")[1];
    saveTotal(lastRow);

}

// ====================
// Event Handling Functions
// ====================
function attachRowEventListeners(row) {
    const multilineFormL = row.querySelector('input[name="multiline_form_L"]');
    if (multilineFormL) {
        multilineFormL.addEventListener("input", () => updateQuantity(row));
    }

    const multilineFormN = row.querySelector('input[name="multiline_form_N"]');
    if (multilineFormN) {
        multilineFormN.addEventListener("input", () => updateQuantity(row));
    }

    const multilineFormW = row.querySelector('input[name="multiline_form_W"]');
    if (multilineFormW) {
        multilineFormW.addEventListener("input", () => updateQuantity(row));
    }

    const multilineFormH = row.querySelector('input[name="multiline_form_H"]');
    if (multilineFormH) {
        multilineFormH.addEventListener("input", () => updateQuantity(row));
    }

    const selectElement = row.querySelector('select[name="multiline_form_code"]');
    if (selectElement) {
        selectElement.addEventListener("change", () => handleDropdownRequest(selectElement));
    }

    const rowFormControls = row.querySelectorAll(".form-control:not(.table-name), .form-select:not(.wall)");
    Array.from(rowFormControls).forEach((formControl) => {
        formControl.addEventListener("change", (event) => setTimeout(() => saveField(event), 200));
    });

    let addRowButtons = row.getElementsByClassName("ar_btn");

    for (let i = 0; i < addRowButtons.length; i++) {
        addRowButtons[i].addEventListener("click", function () {
            let tableType = addRowButtons[i].getAttribute("data-table-type");
            let direction = addRowButtons[i].getAttribute("data-direction");
            addRow(this, tableType,direction);
        });


    }
}

function reattachEventListeners(container) {
    const deleteRowButtons = container.getElementsByClassName("dr_btn");
    for (let i = 0; i < deleteRowButtons.length; i++) {
        deleteRowButtons[i].addEventListener("click", function () {
            let tableID1 = deleteRowButtons[i].getAttribute("data-id1");
            let tableID2 = deleteRowButtons[i].getAttribute("data-id2");
            deleteRow(tableID1, tableID2);
        });
    }

    const duplicateButtons = container.getElementsByClassName("dp_btn");
    for (let i = 0; i < duplicateButtons.length; i++) {
        duplicateButtons[i].addEventListener("click", function () {
            const containerID = duplicateButtons[i].getAttribute("data-id");
            console.log("Button clicked, data-id:", containerID);
            duplicateContainer(containerID);
        });
    }
}

function handleDropdownRequest(selectElement) {
    const selectedValue = selectElement.value;
    const model = selectElement.getAttribute("data-model");
    const field = selectElement.getAttribute("data-field");
    let pkValue;
    if (model == "Floor") {
        pkValue = selectElement.closest("tr").querySelector('input[name="pk_row_floor"]').value;
    } else if (model == "WallMasonry") {
        pkValue = getNthParent(selectElement, 4).querySelector('input[name="pk_row_wall"]').value;
    }
    const value = selectElement.value;
    let tableElement = selectElement.closest("table");
    let table_name = tableElement ? tableElement.id : null;

    if (selectedValue !== "Select Code") {
        fetch("/client/boq_calculation/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
            },
            body: JSON.stringify({
                selected_value: selectedValue,
                model: model,
                field: field,
                pk: projectPK,
            }),
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.totalprice) {
                    let rateperunitField = selectElement.closest("tr").querySelector('input[name="multiline_form_rateperunit"]');
                    rateperunitField.value = parseFloat(data.totalprice).toFixed(2);
                    let unit = data.unit
                    let totalPrice = data.totalprice
                      console.log(data)
                    if (model == "Floor") {
                        let gstRow = getGSTRowByElement(selectElement);
                        let gstValue = totalPrice - data.total_basic_value;  // Calculate GST value
                        let gstPercentage = (gstValue / data.total_basic_value) * 100;
                        let totalBasicAmount = gstRow.querySelector('input[name="mf_totalbasicamount"]');
                        totalBasicAmount.value = data.total_basic_value


                        let gstField = gstRow.querySelector('input[name="mf_gst"]');
                        gstField.value = gstPercentage

                        let gstAmount = gstRow.querySelector('input[name="mf_gstamount"]');
                        gstAmount.value = gstValue

                         let unitSelect = selectElement.closest("tr").querySelector('select[name="multiline_form_unit"]');
                             console.log(unitSelect); // This should not be null or undefined
                              console.log(data.unit)
                            // Check if the unit value exists in data
                                                    if (data.unit) {
                            // Check if the unit value matches one of the option values
                            const unitExists = Array.from(unitSelect.options).some(option => option.value == data.unit);
                            console.log('unitExists:', unitExists); // Log if the unit exists in options

                            if (unitExists) {
                                // Set the select value to the unit ID from data
                                unitSelect.value = data.unit;
                                unitSelect.dispatchEvent(new Event('change')); // Trigger change event if necessary
                                console.log('Updated unitSelect value:', unitSelect.value); // Confirm it's updated
                            } else {
                                console.error("Unit not found in select options.");
                            }
                        } else {
                            console.error("data.unit or unitSelect is missing.");
                        }


                        //updateQuantity(selectElement.closest("tr"));
                    } else if (model == "WallMasonry") {
                        console.log(data)
                        let quantityField = selectElement.closest("tr").querySelector(".total-quantity");
                        let totalAmountField = selectElement.closest("tr").querySelector(".total-amount");
                        let unitField = selectElement.closest("tr").querySelector(".total-unit");

                        unitField.value = data.unit;
                        totalAmountField.value = "₹ " + (parseFloat(rateperunitField.value) * parseFloat(quantityField.value)).toFixed(2);

                        let gstTable = getGSTTableByRow(selectElement.closest("tr"));
                        let gstRow = gstTable.querySelectorAll("tbody")[1];

                        console.log(gstRow)
                        let totalBasicAmount = gstRow.querySelector("input.total-basic-amount");
                        totalBasicAmount.value = "₹ " + data.total_basic_value;

                        let gstField = gstRow.querySelector("input.total-gst");
                        gstField.value = data.total_gst;

                        let gstAmount = gstRow.querySelector("input.total-gst-amount");
                        gstAmount.value = "₹ " + data.totalgstprice;

                        saveTotal(selectElement.closest("tr"), value);
                    }
                } else {
                    console.error("Error fetching data:", data.error);
                }
            });

        $.ajax({
            url: `/client/boq/${projectPK}/`,
            type: "POST",
            contentType: "application/json",
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
            },
            data: JSON.stringify({
                model: model,
                field: "code",
                value: value,
                pk: pkValue,
                table_name: table_name,
            }),
            success: function (response) {
                if (response.pk && pkValue == "new") {
                    const pkField = getNthParent(selectElement, 2).querySelector(".pk_row");
                    pkField.value = response.pk;
                }
            },
            error: function (xhr, status, error) {},
        });
    }
}

function saveTotal(row, codeValue) {
    let gstRow;
    try {
        gstRow = getGSTTableByRow(row).querySelectorAll("tbody")[1].querySelector("tr");
    } catch (error) {
        gstRow = row;
    }

    const obj_pk = row.querySelector('input[name="total_pk"]').value;
    const fieldValues = {
        code: parseFloat(codeValue) || null,
        full_amount: parseFloat(row.querySelector("input.total-amount")?.value.replace(/^\D+/g, "")) || null,
        quantity: parseFloat(row.querySelector("input.total-quantity")?.value.replace(/^\D+/g, "")) || null,
        rate_per_unit: parseFloat(row.querySelector("input.total-full-rate")?.value.replace(/^\D+/g, "")) || null,
        basic_amount: parseFloat(gstRow.querySelector("input.total-basic-amount")?.value.replace(/^\D+/g, "")) || null,
        gst_applied: parseFloat(gstRow.querySelector("input.total-gst")?.value.replace(/^\D+/g, "")) || null,
        gst_amount: parseFloat(gstRow.querySelector("input.total-gst-amount")?.value.replace(/^\D+/g, "")) || null,
    };

    $.ajax({
        url: `/client/boq/${projectPK}/total/`,
        type: "POST",
        contentType: "application/json",
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
        },
        data: JSON.stringify({
            obj_pk: obj_pk,
            fieldValues: fieldValues,
        }),
        success: function (response) {
        },
    });

    updateAbstractTableTotals()


}

function changeTableHeadingName(element) {
    let model = element.getAttribute("data-model");
    let tableID = element.getAttribute("data-value");
    let newName = element.value;

    $.ajax({
        url: `/client/boq/${projectPK}/table-name/`,
        type: "POST",
        contentType: "application/json",
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
        },
        data: JSON.stringify({
            model: model,
            table_id: tableID,
            new_name: newName,
        }),
        success: function (response) {},
    });
}
// ====================
// Row Management Functions
// ====================
function addRow(btn, tableType, direction) {
    let row = btn.closest('tr');
    let tbody = btn.closest('tbody');
    let newRow1 = row.cloneNode(true);
    console.log( newRow1)

    // Clear input, textarea, and select values
    newRow1.querySelectorAll("input, textarea, select").forEach((element) => {
        element.value = "";
    });

    // Remove specific cells (if applicable)

    newRow1.querySelectorAll("td.bg-white").forEach((td) => {
        td.remove();
    });
    const deleteButton = newRow1.querySelector('.del-row-btn');

// Ensure the button exists
if (deleteButton) {
    // Remove the 'disabled' attribute if it exists
    deleteButton.removeAttribute('disabled');

    // Remove the 'disabled' class if it's present
    deleteButton.classList.remove('disabled');

    // Check if everything is correct
    console.log(deleteButton.disabled);  // Should log `false`
    console.log(deleteButton.classList); // Should not include 'disabled'
}



    const tdTextAreaCell = tbody.querySelector("td.bg-white");
    const tdworkvalueCell = tbody.querySelector("td.work-value");
    if (tdworkvalueCell) {
        tdworkvalueCell.rowSpan = (parseInt(tdworkvalueCell.rowSpan) || 1) + 1;
    }
    if (tdTextAreaCell) {
        tdTextAreaCell.rowSpan = (parseInt(tdTextAreaCell.rowSpan) || 1) + 1;
    }

    // Handle different table types and adjust rows accordingly
    if (tableType === "floor") {
        newRow1.querySelector('input[name="pk_row_floor"]').value = "new";
        newRow1.querySelector('input[name="multiline_form_rateperunit"]').value = "0";
        // Fetch the newly cloned row's select element
    let newSelect = newRow1.querySelector('select[name="multiline_form_code"]');

    // Collect already selected values from other rows
    let selectedValues = [];
    tbody.querySelectorAll('select[name="multiline_form_code"]').forEach((select) => {
        if (select !== newSelect) {
            selectedValues.push(select.value);
        }
    });

    // Loop through options in the new select element and hide already selected options
    newSelect.querySelectorAll('option').forEach((option) => {
        if (selectedValues.includes(option.value)) {
            option.disabled = true; // Hide the option by disabling it
        } else {
            option.disabled = false; // Ensure it's enabled if not selected in other rows
        }
    });
    }
    if (tableType === "wall") {
        newRow1.querySelector('input[name="pk_row_wall"]').value = "new";
        newRow1.querySelectorAll("td.code-td, td.unit-td, td.rate-td, td.amount-td").forEach((element) => {
            element.remove();
        }
        );

        let codeTD = tbody.querySelector("td.code-td");
        if (codeTD) {
            codeTD.rowSpan = (parseInt(tdTextAreaCell.rowSpan) || 1) + 1;
        }
        let unitTD = tbody.querySelector("td.unit-td");
        if (unitTD) {
            unitTD.rowSpan = (parseInt(tdTextAreaCell.rowSpan) || 1) + 1;
        }
        let rateTD = tbody.querySelector("td.rate-td");
        if (rateTD) {
            rateTD.rowSpan = (parseInt(tdTextAreaCell.rowSpan) || 1) + 1;
        }
        let amountTD = tbody.querySelector("td.amount-td");
        if (amountTD) {
            amountTD.rowSpan = (parseInt(tdTextAreaCell.rowSpan) || 1) + 1;
        }
    }
    if (tableType === "finishing") {
        newRow1.querySelector('input[name="pk_row_product"]').value = "new";
    }
    if (tableType === "other") {
        newRow1.querySelector('input[name="pk_row_other"]').value = "new";
        newRow1.querySelectorAll("td.work-value").forEach((td) => {
            td.remove();
        });

        //row.querySelector('td.work-value').rowSpan = (parseInt(tdTextAreaCell.rowSpan) || 1) + 1;
    }

    attachRowEventListeners(newRow1);

    // Insert newRow1 based on direction
    if (direction === 'above') {
        row.insertAdjacentElement('beforebegin', newRow1); // Insert newRow above the current row
    } else {
        row.insertAdjacentElement('afterend', newRow1); // Insert newRow below the current row
    }

    // Handle the last GST row, if it exists
    let lastRow2 = getGSTRowByElement(btn);
    if (lastRow2) {
        let newRow2 = lastRow2.cloneNode(true);

        newRow2.querySelectorAll("input").forEach((element) => {
            element.value = "";
        });

        attachRowEventListeners(newRow2);

        // Insert newRow2 based on direction
        if (direction === 'above') {
            lastRow2.insertAdjacentElement('beforebegin', newRow2); // Insert newRow above
        } else {
            lastRow2.insertAdjacentElement('afterend', newRow2); // Insert newRow below
        }
    }

}




// ====================
// Container Management Functions
// ====================
function duplicateContainer(containerID) {
    // Find the container by its ID
    const container = document.getElementById(containerID).parentNode;
    console.log("Container to be duplicated:", container);

    if (!container) {
        console.error("Container with ID", containerID, "not found.");
        return;
    }

    const containerClone = container.cloneNode(true);

    updateElementIDs(containerClone);

    containerClone.id = `${containerID}_clone_${new Date().getTime()}`;

    container.parentNode.insertBefore(containerClone, container.nextSibling);
      reattachEventListeners(containerClone);
    console.log("Container duplicated successfully:", containerClone);



}

function reattachEventListeners(containerClone) {
    // Reattach 'Add Row' button listeners for the duplicated container
    containerClone.querySelectorAll(".add-row-btn").forEach(button => {
        button.addEventListener("click", function (event) {
            const direction = button.getAttribute("data-direction"); // Get the direction from data attribute
            const tableType = button.getAttribute("data-table-type"); // Get the table type from data attribute

            // Make sure to pass the button and correct parameters to addRow
            addRow(button, tableType, direction); // Call addRow with the correct parameters
        });
    });
}

// Table Management Functions
// ====================
function updateAbstractTableTotals() {
    let totals = document.querySelectorAll(".total-basic-amount");
    let tableKeyTotal = {};
    totals.forEach((element) => {
        tableKeyTotal[element.closest("tr").querySelector('input[name="mainTable"]').value] = element.value;
    });

    for (const key in tableKeyTotal) {
        const row = document.querySelector(`tr[data-table-key="${key}"]`);
        if (row) {
            const excludingGstField = row.querySelector('input[name="abstract_form_excludinggst"]');
            const fullAmountField = row.querySelector('input[name="abstract_form_fullamount"]');
            const ratioField = row.querySelector('input[name="abstract_form_ratio"]');
            const gstField = row.querySelector('select[name="abstract_form_gst"]');
            const gstValue = parseFloat(gstField.options[gstField.selectedIndex].text) || 0


            let gstRow = getGSTRowByElement(ratioField)

            let basicAmountField = gstRow.querySelector('input[name="af_totalbasicamount"]');
            let gstAppliedField = gstRow.querySelector('input[name="af_gst"]');
            let gstAmountField = gstRow.querySelector('input[name="af_gstamount"]');
                       if (excludingGstField) {
                excludingGstField.value = tableKeyTotal[key];
            }

            const totalKeyValue = parseFloat(tableKeyTotal[key].replace(/^\D+/g, ""));
            const calculatedBasicAmount = ((totalKeyValue * parseFloat(ratioField.value / 100))).toFixed(2);
            basicAmountField.value = calculatedBasicAmount;
            let bs_amount= calculatedBasicAmount

            if (gstValue != 0) {
                const calculatedGstAmount = ((calculatedBasicAmount * parseFloat(gstValue / 100))).toFixed(2);
                basicAmountField.value = parseFloat(bs_amount).toFixed(2);
                gstAmountField.value = calculatedGstAmount;
                fullAmountField.value = (parseFloat(bs_amount) + parseFloat(gstAmountField.value)).toFixed(2);

                gstAppliedField.value = ((parseFloat(gstAmountField.value) / calculatedBasicAmount) * 100).toFixed(0) + "%";
            } else {
                gstAmountField.value = 0;
                gstAppliedField.value = 0;
            }

            if (fullAmountField) {
                fullAmountField.value = (parseFloat(bs_amount) + parseFloat(gstAmountField.value)).toFixed(2);
            }


        }
    }
}


function hideShowTable(tableID) {
    let table = document.getElementById(tableID);
    table.classList.toggle("d-none");
}

function collapseTable(tableList){
    tableList.forEach((element) => {
        document.getElementById(element).querySelector('tbody').classList.toggle('d-none');
    })
}

// ====================
// Calculation Functions
// ====================
let tableTotals = {};

function calculateTotal() {

    // Select all tables with the relevant input fields
    const tables = document.querySelectorAll("table");

    tables.forEach((table) => {
        let total = 0;

        const fullAmountFields = table.querySelectorAll('input[name="multiline_form_fullamount"]');
        if (fullAmountFields.length != 0) {
            fullAmountFields.forEach((field) => {
                const value = parseFloat(field.value) || 0;
                total += value;
            });
            const totalField = table.querySelector(".total-amount");
            totalField.value =  total.toFixed(2);
            tableTotals[table.id] = total.toFixed(2);
        }

        const basicAmountFields = table.querySelectorAll('input[name="mf_totalbasicamount"]');
        if (basicAmountFields.length != 0) {
            total = 0;
            basicAmountFields.forEach((field) => {
                const value = parseFloat(field.value) || 0;
                total += value;
            });
            const totalField = table.querySelector(".total-basic-amount");
            totalField.value =  total.toFixed(2);
            updatereportform()

        }

        const finishingbasicAmountFields = table.querySelectorAll('input[name="bf_totalbasicamount"]');
        if (finishingbasicAmountFields.length != 0) {
            total = 0;
            finishingbasicAmountFields.forEach((field) => {
                const value = parseFloat(field.value) || 0;
                total += value;
            });
            const totalField = table.querySelector(".total-basic-amount");
            totalField.value = total.toFixed(2);
            updatereportform()
        }

        const finishingfullamountFields = table.querySelectorAll('input[name="basicform_fullamount"]');
        if (finishingfullamountFields.length != 0) {
            total = 0;
            finishingfullamountFields.forEach((field) => {
                const value = parseFloat(field.value) || 0;
                total += value;
            });
            const totalField = table.querySelector(".total-amount");
            totalField.value =  total.toFixed(2);
        }
        const otherAmountFields = table.querySelectorAll('input[name="percentage_form_fullamount"]');
        if (otherAmountFields.length != 0) {
            total = 0;
            otherAmountFields.forEach((field) => {
                const value = parseFloat(field.value) || 0;
                total += value;
            });
            const totalField = table.querySelector(".total-other-amount");
            totalField.value = total.toFixed(2);
        }

        const gstFields = table.querySelectorAll('input[name="mf_gst"]');
        if (gstFields.length != 0) {
            total = 0;
            gstFields.forEach((field) => {
                const value = parseFloat(field.value) || 0;
                total += value;
            });
            total = total / gstFields.length;
            const totalField = table.querySelector(".total-gst");
            totalField.value = total.toFixed(2) + "%";
        }
        const finishinggstFields = table.querySelectorAll('input[name="bf_gst"]');
        if (finishinggstFields.length != 0) {
            total = 0;
            finishinggstFields.forEach((field) => {
                const value = parseFloat(field.value) || 0;
                total += value;
            });
            total = total / finishinggstFields.length;
            const totalField = table.querySelector(".total-gst");
            totalField.value = total + "%";
        }

        const gstAmountFields = table.querySelectorAll('input[name="mf_gstamount"]');
        if (gstAmountFields.length != 0) {
            total = 0;
            gstAmountFields.forEach((field) => {
                const value = parseFloat(field.value) || 0;
                total += value;
            });
            const totalField = table.querySelector(".total-gst-amount");
            totalField.value =  total.toFixed(2);
        }
        const basicformgstAmountFields = table.querySelectorAll('input[name="bf_gstamount"]');
        if (basicformgstAmountFields.length != 0) {
            total = 0;
            basicformgstAmountFields.forEach((field) => {
                const value = parseFloat(field.value) || 0;
                total += value;
            });
            const totalField = table.querySelector(".total-gst-amount");
            totalField.value =  total.toFixed(2);

        }

        const quantityAmountFields = table.querySelectorAll('input[name="multiline_form_quantity"]');
        const totalQuantityField = table.querySelector(".total-quantity");
        let quantity = 0;
        if (quantityAmountFields.length != 0 && totalQuantityField) {
            quantityAmountFields.forEach((field) => {
                const value = parseFloat(field.value) || 0;
                quantity += value;
            });
            totalQuantityField.value = quantity.toFixed(2);
        }

        const wallTotalAmount = table.querySelector(".wall.total-amount");
        const wallRateAmount = table.querySelector(".total-full-rate");
        if (wallRateAmount && wallTotalAmount) {
            wallTotalAmount.value = (parseFloat(totalQuantityField.value) * parseFloat(wallRateAmount.value)).toFixed(2);
        }

        const valueExcludingGSTFields = table.querySelectorAll('input[name="abstract_form_excludinggst"]');
        if (valueExcludingGSTFields.length != 0){
            total = 0;
            valueExcludingGSTFields.forEach((field) => {
                const value = parseFloat(field.value.replace(/^\D+/g, "")) || 0;
                total += value;
            });
            const totalField = table.querySelector(".total-value-off-gst");
            totalField.value =   total.toFixed(2);
        }

        const ratioFields = table.querySelectorAll('input[name="abstract_form_ratio"]');
        if(ratioFields.length != 0){
            let totalRatio = 0;
            ratioFields.forEach((field) =>{
                const value = parseFloat(field.value) || 1.00;
                totalRatio += value;
            });
            const totalRatioField = table.querySelector(".total-ratio");
            totalRatioField.value =  parseFloat(totalRatio/ratioFields.length).toFixed(2);
        }

        const abstractFullAmountFields = table.querySelectorAll('input[name="abstract_form_fullamount"]');
        if (abstractFullAmountFields.length != 0){
            total = 0;
            abstractFullAmountFields.forEach((field) => {
                const value = parseFloat(field.value.replace(/^\D+/g, "")) || 0;
                total += value;
            });
            const totalField = table.querySelector(".total-full-amount");
            totalField.value =   total.toFixed(2);
        }

        const abstractGSTFields = table.querySelectorAll('input[name="af_gst"]');
        if (abstractGSTFields.length != 0){
            total = 0;
            abstractGSTFields.forEach((field) => {
                const value = parseFloat(field.value.replace(/^\D+/g, "")) || 0;
                total += value;
            });
            const totalField = table.querySelector(".total-gst");
            totalField.value =  (total/abstractGSTFields.length).toFixed(2) + "%";
        }
        const abstractGSTAmountFields = table.querySelectorAll('input[name="af_gstamount"]');
        if (abstractGSTAmountFields.length != 0){
            total = 0;
            abstractGSTAmountFields.forEach((field) => {
                const value = parseFloat(field.value.replace(/^\D+/g, "")) || 0;
                total += value;
            });
            const totalField = table.querySelector(".total-gst-amount");
            totalField.value =   total.toFixed(2);
        }

        const abstractBasicAmountFields = table.querySelectorAll('input[name="af_totalbasicamount"]');
        if (abstractBasicAmountFields.length != 0){
            total = 0;
            abstractBasicAmountFields.forEach((field) => {
                const value = parseFloat(field.value.replace(/^\D+/g, "")) || 0;
                total += value;
            });
            const totalField = table.querySelector(".total-basic-amount");
            totalField.value =   total.toFixed(2);
        }
    });
    updateAbstractTableTotals();
    calculateWorkValue();
     updatereportform()
}

function calculateWorkValue() {
    let totalFields = document.querySelectorAll(".total-amount");
    const workValueField = document.getElementsByClassName("work-values")[0];
    let total = 0;

    totalFields.forEach((field) => {
        let value = field.value.trim();

        value = value.replace(/[^\d.-]/g, "") || "0";
        const parsedValue = parseFloat(value);

        if (isNaN(parsedValue)) {
            console.error(`Invalid number: ${value}`);
        } else {
            total += parsedValue;
        }
    });

    if (workValueField) {
        workValueField.value = total.toFixed(2);
    }

    let rows = workValueField.closest("tbody").querySelectorAll("tr.table-row");
    rows.forEach((row) => {
        const ratio = row.querySelector('input[name="percentage_form_ratio"]').value;
        const gstSelect = row.querySelector('select[name="percentage_form_gst"]');
        const gstValue =  gstSelect.options[gstSelect.selectedIndex].text || 0;
        const fullAmount = row.querySelector('input[name="percentage_form_fullamount"]');

        const basicAmount = (workValueField.value * (ratio / 100)).toFixed(2);
        const gstAmount = (parseFloat(basicAmount) * parseFloat(gstValue / 100)).toFixed(2);
        const fullAmountTotal = parseFloat(basicAmount) + parseFloat(gstAmount);
        fullAmount.value = parseFloat(fullAmountTotal).toFixed(2);

        const gstRow = getGSTRowByElement(fullAmount);
        gstRow.querySelector('input[name="bf_totalbasicamount"]').value = basicAmount;
        gstRow.querySelector('input[name="bf_gst"]').value = gstValue;
        gstRow.querySelector('input[name="bf_gstamount"]').value = gstAmount;
    });
}

function calculateFinishingRow(element) {
    let row = element.closest("tr");
    let basicPrice = row.querySelector('input[name="basicform_basicrate"]').value;
    let quantity = row.querySelector('input[name="basicform_quantity"]').value;
    let fullRate = row.querySelector('input[name="basicform_fullrate"]');
    let gstSelect = row.querySelector('select[name="basicform_gst"]');
    let gstValue = gstSelect.options[gstSelect.selectedIndex].text || 0;
    let fullAmount = row.querySelector('input[name="basicform_fullamount"]');

    let gstRow = getGSTRowByElement(element);

    let totalBasicAmountField = gstRow.querySelector('input[name="bf_totalbasicamount"]');
    let gstAppliedField = gstRow.querySelector('input[name="bf_gst"]');
    let gstAmountField = gstRow.querySelector('input[name="bf_gstamount"]');

    fullRate.value = parseFloat(basicPrice) * parseFloat(quantity);
    totalBasicAmountField.value = fullRate.value;
    if (gstValue == "Select") {
        fullAmount.value = fullRate.value;
        gstAppliedField.value = 0;
        gstAmountField.value = 0;
    } else {
        fullAmount.value = parseFloat(gstValue / 100) * parseFloat(fullRate.value) + parseFloat(fullRate.value);
        gstAppliedField.value = gstValue;
        gstAmountField.value = parseFloat(gstValue / 100) * parseFloat(fullRate.value);
    }
}

// ====================
// Initialization
// ====================
document.addEventListener("DOMContentLoaded", function () {
    let deleteRowButtons = document.getElementsByClassName("dr_btn");
    for (let i = 0; i < deleteRowButtons.length; i++) {
        deleteRowButtons[i].addEventListener("click", function () {
            let pk = deleteRowButtons[i].getAttribute("data-pk");
            let tableType = deleteRowButtons[i].getAttribute("data-table-type");
            deleteRow(pk, tableType);
        });
    }

    document.querySelectorAll(".dp_btn").forEach((button) => {
        button.addEventListener("click", function () {
            const containerID = button.getAttribute("data-id");
            console.log("Button clicked, data-id:", containerID);
            duplicateContainer(containerID);
        });
    });


    let collapseButtons = document.getElementsByClassName("c_btn");
    Array.from(collapseButtons).forEach((element) => {
        element.addEventListener("click", function() {
            const mainTableID = this.getAttribute("data-main-table");
            const secondaryTableID = this.getAttribute("data-secondary-table");
            const tablesToCollapse = [mainTableID, secondaryTableID];

            collapseTable(tablesToCollapse);
        });
    });

    let gstBtns = document.querySelectorAll(".gst_btn");
    gstBtns.forEach((element) => {
        element.addEventListener("click", function () {
            hideShowTable(element.getAttribute("data-id"));
        });
    });
    const existingRows = document.querySelectorAll(".table-row");
    existingRows.forEach((row) => attachRowEventListeners(row));

    const tableHeadingFields = document.querySelectorAll("input[name='table-heading-name']");
    tableHeadingFields.forEach((field) => {
        field.addEventListener("focusout", function () {
            changeTableHeadingName(this);
        });
    });

    let totalFields = document.querySelectorAll(".total-amount, input[name='percentage_form_ratio'], select[name='percentage_form_gst']");
    totalFields.forEach((field) => {
        field.addEventListener("change", calculateWorkValue);
    });

    let finishingFields = document.querySelectorAll('input[name="basicform_basicrate"], input[name="basicform_quantity"], input[name="basicform_fullrate"], input[name="basicform_fullamount"], select[name="basicform_gst"]');
    finishingFields.forEach((field) => {
        field.addEventListener("change", function () {
            calculateFinishingRow(this);
        });
    });
    setInterval(calculateTotal, 1000);
});

function deleteRowFromBackend(pk, tableType) {
    let csrfToken = document.getElementById('csrf_token').value; // Get CSRF token


    return fetch('/client/deleterow/',{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({
            pk: pk,
            table_type: tableType,
        }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json(); // Ensure this returns a promise
    })
    .then(data => {
        if (data.success) {

            return true; // Return true to indicate success
        } else {

            return false; // Return false to indicate failure
        }
    })
    .catch(error => {
        console.error('Error:', error);
        return false; // Return false if there was an error
    });
}

function deleteRow(button, tableType, pk) {
    // Optional: Send an AJAX request to delete the row from the backend
    deleteRowFromBackend(pk, tableType)
        .then(success => {
            if (success) {
                // If the backend deletion was successful, remove the main row and the GST row
                let row = button.closest('tr'); // Find the closest <tr> to the delete button

                if (row) {
                    let gstRow = getGSTRowByElement(button); // Use the same logic as in the addRow function

                    if (gstRow) {
                        gstRow.remove(); // Remove the GST row if it exists
                    }

                    row.remove(); // Remove the main row
                }
            } else {
                // If deletion from the backend failed, still remove the row on the frontend
                let row = button.closest('tr');
                let gstRow = getGSTRowByElement(button); // Fetch the GST row

                if (gstRow) {
                    gstRow.remove(); // Remove the GST row
                }

                row.remove(); // Remove the main row
            }
        })
        .catch(error => {
            console.error("Error while deleting row:", error);
        });
}


function updateDeleteButtons() {
    // Select all delete buttons
    const deleteButtons = document.querySelectorAll('.del-row-btn1');
console.log(deleteButtons)
    // Get the number of rows in the table
    const tableRows = document.querySelectorAll('.floor1');
   console.log( tableRows.length )
    // If only one row exists, disable all delete buttons
    if (tableRows.length === 1) {
        deleteButtons.forEach(button => {
            button.disabled = true;
             button.setAttribute('disabled', 'true');
              button.classList.add('disabled');
        });
    } else {
        deleteButtons.forEach(button => {
            button.disabled = false;
             button.classList.remove('disabled');
        });
    }
}
function updatereportform() {
    let totalBasicAmount = 0;
    let totalGST = 0;
    let totalGSTAmount = 0;
      const gstRefundPercentageInput = document.getElementById('gstRefundPercentage');
    const totalWorkAmountInput = document.getElementById('totalWorkAmount');
     const gstToBeCollectedPercentageInput = document.getElementById('gstToBeCollectedPercentage');
      const gstRefundBenefitInput = document.getElementById('gstRefundBenefit');
      const gstPercentageToBePaidInput = document.getElementById('gstPercentageToBePaid');
      const gstToBePaidInput = document.getElementById('gstToBePaid');
       const gstToBeCollectedInput = document.getElementById('gstToBeCollected');
       const totalAmountInput = document.getElementById('totalAmount');

    // Sum values from all .total-basic-amount fields across all tables
    document.querySelectorAll(".total-basic-amount").forEach(element => {
        totalBasicAmount += parseFloat(element.value) || 0;
    });
     totalWorkAmountInput.value = totalBasicAmount.toFixed(2);
    // Sum values from all .total-gst fields across all tables

    // Sum values from all .total-gst-amount fields across all tables
    document.querySelectorAll(".total-gst-amount").forEach(element => {
        totalGSTAmount += parseFloat(element.value) || 0;
    });

    totalGST += parseFloat( totalBasicAmount)/ parseFloat(totalGSTAmount);
      gstRefundPercentageInput.value =  totalGST.toFixed(2);
      gstToBeCollectedPercentageInput.value =parseFloat(18.00)-parseFloat(totalGST)
      const gstRefund = (parseFloat(totalBasicAmount) * parseFloat(totalGST)) / 100;
      gstRefundBenefitInput.value = gstRefund.toFixed(2);
      const gstToBePaid = (parseFloat(totalBasicAmount) * parseFloat(18)) / 100;
      gstToBePaidInput.value = gstToBePaid.toFixed(2);
      const gstToBeCollectedPercentage = parseFloat(gstToBeCollectedPercentageInput.value) || 0;
      const gstToBeCollected = (totalBasicAmount * gstToBeCollectedPercentage) / 100;
      const totalAmount = totalBasicAmount + gstToBePaid + gstRefund + gstToBeCollected;
      gstToBeCollectedInput.value = gstToBeCollected.toFixed(2);
      totalAmountInput.value = totalAmount.toFixed(2);
    // Update disabled input fields with the calculated totals
    document.querySelectorAll("input[name='basic_value']").forEach(input => {
        input.value = totalBasicAmount.toFixed(2);
    });

    document.querySelectorAll("input[name='gst']").forEach(input => {
        input.value = totalGST.toFixed(2);
    });

    document.querySelectorAll("input[name='gst_value']").forEach(input => {
        input.value = totalGSTAmount.toFixed(2);
    });
}
window.addEventListener('load', updatereportform);
document.querySelectorAll('.total-basic-amount, .total-gst, .total-gst-amount').forEach(input => {
    input.addEventListener('input', updatereportform);
});




