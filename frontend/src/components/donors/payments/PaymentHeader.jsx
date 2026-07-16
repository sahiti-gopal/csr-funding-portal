import { Plus, ChevronDown } from "lucide-react";

export default function PaymentHeader({
  donor,
  donors,
  onChange,
}) {

  return (

    <div className="payment-header">

      <div className="payment-header-left">

        <div className="payment-avatar">

          {donor?.name
            ?.split(" ")
            .map((x) => x[0])
            .join("")
            .slice(0, 2)}

        </div>

        <div className="payment-header-info">

          <h2>

            {donor?.name || "Select Donor"}

          </h2>

          <p>

            {donor?.focus_area || "CSR Donor"}

          </p>

        </div>

        <div className="payment-select">

          <select

            value={donor?.id || ""}

            onChange={(e) =>
              onChange(e.target.value)
            }

          >

            {donors.map((item) => (

              <option

                key={item.id}

                value={item.id}

              >

                {item.name}

              </option>

            ))}

          </select>

          <ChevronDown
            size={18}
            className="select-icon"
          />

        </div>

      </div>

      <div className="payment-header-right">

        <button className="payment-add-btn">

          <Plus size={18} />

          Add Donor

        </button>

      </div>

    </div>

  );

}