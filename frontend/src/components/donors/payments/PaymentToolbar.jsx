import {
  Search,
  Download,
  RotateCw,
  Filter,
} from "lucide-react";

export default function PaymentToolbar({
  search,
  onSearch,

  statusFilter,
  setStatusFilter,

  fyFilter,
  setFyFilter,

  onRefresh,
  onDownload,
}) {

  return (

    <div className="payment-toolbar">

      <div className="payment-toolbar-left">

        <div className="payment-search">

          <Search size={18} />

          <input
            type="text"
            placeholder="Search installments, UTR, payment mode..."
            value={search}
            onChange={(e) =>
              onSearch(e.target.value)
            }
          />

        </div>

      </div>

      <div className="payment-toolbar-right">

        <div className="toolbar-filter">

          <Filter size={16} />

          <select
            value={statusFilter}
            onChange={(e) =>
              setStatusFilter(e.target.value)
            }
          >
            <option value="All">
              All Status
            </option>

            <option value="Paid">
              Paid
            </option>

            <option value="Pending">
              Pending
            </option>

            <option value="Scheduled">
              Scheduled
            </option>

            <option value="Overdue">
              Overdue
            </option>

          </select>

        </div>

        <div className="toolbar-filter">

          <select
            value={fyFilter}
            onChange={(e) =>
              setFyFilter(e.target.value)
            }
          >

            <option value="All">
              All FY
            </option>

            <option value="2024">
              FY 2024
            </option>

            <option value="2025">
              FY 2025
            </option>

            <option value="2026">
              FY 2026
            </option>

            <option value="2027">
              FY 2027
            </option>

          </select>

        </div>

        <button
          className="toolbar-btn secondary"
          onClick={onRefresh}
        >

          <RotateCw size={16} />

          Refresh

        </button>

        <button
          className="toolbar-btn primary"
          onClick={onDownload}
        >

          <Download size={16} />

          Download CSV

        </button>

      </div>

    </div>

  );

}