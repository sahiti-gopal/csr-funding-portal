import { useMemo, useState } from "react";
import {
  ArrowUpDown,
  Copy,
  CheckCircle2,
} from "lucide-react";

import StatusBadge from "./StatusBadge";

export default function PaymentSchedule({
  rows = [],
}) {
  const [sortField, setSortField] =
    useState("due");

  const [ascending, setAscending] =
    useState(true);

  const sortedRows = useMemo(() => {
    const arr = [...rows];

    arr.sort((a, b) => {
      let x = a[sortField];
      let y = b[sortField];

      if (
        sortField === "amount"
      ) {
        x = Number(a.amount);
        y = Number(b.amount);
      }

      if (x == null) return 1;
      if (y == null) return -1;

      if (x > y)
        return ascending ? 1 : -1;

      if (x < y)
        return ascending ? -1 : 1;

      return 0;
    });

    return arr;
  }, [
    rows,
    sortField,
    ascending,
  ]);

  const changeSort = (field) => {
    if (field === sortField) {
      setAscending(!ascending);
    } else {
      setSortField(field);
      setAscending(true);
    }
  };

  const formatMoney = (value) => {
    return new Intl.NumberFormat(
      "en-IN",
      {
        style: "currency",
        currency: "INR",
        maximumFractionDigits: 0,
      }
    ).format(value || 0);
  };

  return (
    <div className="payment-schedule-card">

      <div className="section-header">

        <div>

          <h3>
            Payment Schedule
          </h3>

          <p>
            Installment-wise payment
            tracking
          </p>

        </div>

      </div>

      <div className="payment-table-wrapper">

        <table className="payment-table">

          <thead>

            <tr>

              <th
                onClick={() =>
                  changeSort(
                    "installment"
                  )
                }
              >
                Installment
                <ArrowUpDown
                  size={15}
                />
              </th>

              <th
                onClick={() =>
                  changeSort("due")
                }
              >
                Due Date
                <ArrowUpDown
                  size={15}
                />
              </th>

              <th
                onClick={() =>
                  changeSort(
                    "amount"
                  )
                }
              >
                Amount
                <ArrowUpDown
                  size={15}
                />
              </th>

              <th>
                Received
              </th>

              <th>
                Mode
              </th>

              <th>
                Transaction
              </th>

              <th>
                Status
              </th>

            </tr>

          </thead>

          <tbody>

            {sortedRows.map(
              (row) => (

                <tr
                  key={row.id}
                >

                  <td>

                    <div className="installment-name">

                      {row.installment}

                    </div>

                  </td>

                  <td>
                    {row.due || "-"}
                  </td>

                  <td>

                    <strong>

                      {formatMoney(
                        row.amount
                      )}

                    </strong>

                  </td>

                  <td>
                    {row.received ||
                      "-"}
                  </td>

                  <td>
                    {row.paymentMode ||
                      "-"}
                  </td>

                  <td>

                    <div
                      className="transaction-id"
                      style={{
                        display:
                          "flex",
                        gap: 8,
                        alignItems:
                          "center",
                      }}
                    >

                      <span>

                        {row.transactionId ||
                          "-"}

                      </span>

                      {row.transactionId && (

                        <Copy
                          size={15}
                          style={{
                            cursor:
                              "pointer",
                          }}
                          onClick={() =>
                            navigator.clipboard.writeText(
                              row.transactionId
                            )
                          }
                        />

                      )}

                    </div>

                  </td>

                  <td>

                    <StatusBadge
                      status={
                        row.status
                      }
                    />

                  </td>

                </tr>

              )
            )}

            {sortedRows.length ===
              0 && (
              <tr>

                <td
                  colSpan={7}
                  style={{
                    textAlign:
                      "center",
                    padding:
                      "40px",
                  }}
                >
                  <CheckCircle2
                    size={28}
                    style={{
                      marginBottom:
                        8,
                    }}
                  />

                  <div>
                    No payments
                    found
                  </div>

                </td>

              </tr>
            )}

          </tbody>

        </table>

      </div>

    </div>
  );
}