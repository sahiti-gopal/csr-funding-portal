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
    <div className="overview-grid payment-kpis">

      {data.map((item, index) => {

        const Icon =
          Object.values(icons)[index];

        return (

          <div
            key={item.title}
            className="overview-card stat-card"
          >

            <span className="stat-icon">
              <Icon size={15} />
            </span>

            <span className="eyebrow">
              {item.title}
            </span>

            <div className="overview-value">
              {item.value}
            </div>

          </div>

        );

      })}

    </div>
  );
}