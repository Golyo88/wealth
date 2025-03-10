export enum Role {
  ORSZAGGYULESI_KEPVISELO = 'országgyűlési képviselő',
  HAZAS_ELETTARS = 'házas-/élettárs',
  GYERMEK = 'gyermek',
}

export interface Person {
  name: string;
  role: Role;
}

export interface RealEstate {
  location: string;
  area_m2: number;
  land_use: string;
  building_type?: string;
  building_size_m2?: number;
  legal_status?: string;
  ownership_status: string;
  ownership_share: string;
  acquisition_mode: string;
  acquisition_date: string;
}

export interface Vehicle {
  type: string;
  brand_model: string;
  acquisition_year: number;
  acquisition_mode: string;
}

export interface Security {
  type: string;
  value_huf: number;
}

export interface Savings {
  deposit_huf?: number;
  cash_huf?: number;
  bank_balance_huf?: number;
  bank_balance_foreign_currency?: number;
  exchange_rate?: number;
}

export interface Assets {
  real_estate?: RealEstate[];
  vehicles?: Vehicle[];
  securities?: Security[];
  savings?: Savings;
}

export interface Liabilities {
  public_debt_huf?: number;
  bank_loans_huf?: number;
  private_loans_huf?: number;
}

export interface IncomeItem {
  position: string;
  income_category: string;
}

export interface EconomicInterest {
  organization: string;
  role: string;
  ownership_percentage?: string;
  income_category: string;
}

export interface Wealth {
  id: number;
  person: Person;
  assets: Assets;
  liabilities: Liabilities;
  income: IncomeItem[];
  economic_interests: EconomicInterest[];
}

export interface PaginatedResponse<T> {
  results: T[];
  pagination: {
    page: number;
    page_size: number;
    total: number;
    total_pages: number;
  };
}

export interface WealthFilters {
  name?: string;
  real_estates_count_op?: 'eq' | 'gt' | 'lt';
  real_estates_count?: number;
  vehicles_count_op?: 'eq' | 'gt' | 'lt';
  vehicles_count?: number;
  securities_count_op?: 'eq' | 'gt' | 'lt';
  securities_count?: number;
  income_count_op?: 'eq' | 'gt' | 'lt';
  income_count?: number;
  savings_amount_op?: 'eq' | 'gt' | 'lt';
  savings_amount?: number;
  liabilities_amount_op?: 'eq' | 'gt' | 'lt';
  liabilities_amount?: number;
  net_worth_op?: 'eq' | 'gt' | 'lt';
  net_worth?: number;
  order_by?:
    | 'real_estates_count'
    | 'vehicles_count'
    | 'securities_count'
    | 'income_count'
    | 'savings_amount'
    | 'liabilities_amount'
    | 'net_worth';
  order_direction?: 'asc' | 'desc';
}
