import {
  Wallet,
  CircleDollarSign,
  Clock3,
  Landmark,
  TrendingUp,
  PiggyBank,
} from "lucide-react";

const icons = {
  committed: Wallet,
  received: CircleDollarSign,
  pending: Clock3,
  fy: Landmark,
  utilized: TrendingUp,
  balance: PiggyBank,
};

export default function PaymentKPIs({ data }) {
  return (
    <div className="payment-kpis">

      {data.map((item, index) => {

        const Icon =
          Object.values(icons)[index];

        return (

          <div
            key={item.title}
            className="payment-kpi-card"
          >

            <div className="kpi-header">

              <div
                className="kpi-icon"
                style={{
                  color: item.color,
                }}
              >
                <Icon size={22} />
              </div>

            </div>

            <div
              className="kpi-value"
              style={{
                color: item.color,
              }}
            >
              {item.value}
            </div>

            <div className="kpi-title">

              {item.title}

            </div>

            <div className="kpi-progress">

              <div
                className="kpi-progress-fill"
                style={{
                  background: item.color,
                  width: `${55 + index * 7}%`,
                }}
              />

            </div>

          </div>

        );

      })}

    </div>
  );
}