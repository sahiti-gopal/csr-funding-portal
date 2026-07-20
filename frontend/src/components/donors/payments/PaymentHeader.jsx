import { ChevronDown } from "lucide-react";

export default function PaymentHeader({
  donor,
  donors,
  onChange,
}) {

  return (

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

  );

}
