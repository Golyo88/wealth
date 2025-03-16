export enum Role {
  ORSZAGGYULESI_KEPVISELO = 'országgyűlési képviselő',
  HAZAS_ELETTARS = 'házas-/élettárs',
  GYERMEK = 'gyermek',
}

export interface Person {
  name: string;
  role: Role;
}

export interface PersonView extends Person {
  id: number;
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

export interface MotorVehicle {
  type: string;
  brand_model: string;
  acquisition_year: number;
  acquisition_mode: string;
}

export interface WatercraftOrAircraft {
  type: string;
  brand_model: string;
  acquisition_year: number;
  acquisition_mode: string;
}

export interface Vehicles {
  motor_vehicle?: MotorVehicle[];
  watercraft_or_aircraft?: WatercraftOrAircraft[];
}

export interface Artwork {
  name: string;
  quantity: number;
  acquisition_year: number;
  acquisition_mode: string;
}

export interface Collection {
  name: string;
  quantity: number;
  acquisition_year: number;
  acquisition_mode: string;
}

export interface Artworks {
  artworks?: Artwork[];
  collections?: Collection[];
}

export interface OtherAssets {
  name: string;
  acquisition_year: number;
  acquisition_mode: string;
}

export interface Security {
  type: string;
  value_huf: number;
}

export interface SavingsDeposit {
  value_huf: number;
  exchange_rate?: number;
}

export interface Cash {
  value_huf: number;
  exchange_rate?: number;
}

export interface BankDepositClaim {
  value_huf: number;
  foreign_currency_value_in_huf?: string;
  exchange_rate?: number;
}

export interface OtherClaims {
  value_huf: number;
  exchange_rate?: number;
}

export interface Claims {
  bank_deposit_claims?: BankDepositClaim[];
  other_claims?: OtherClaims[];
}

export interface OtherProperty {
  name: string;
}

export interface Assets {
  real_estate?: RealEstate[];
  vehicles?: Vehicles;
  artworks?: Artworks;
  other_assets?: OtherAssets[];
  securities?: Security[];
  savings_deposit?: SavingsDeposit[];
  cash?: Cash[];
  claims?: Claims;
  other_property?: OtherProperty[];
}

export interface PublicDebt {
  value_huf: number;
  exchange_rate?: number;
}

export interface BankLoan {
  value_huf: number;
  exchange_rate?: number;
}

export interface PrivateLoan {
  value_huf: number;
  exchange_rate?: number;
}

export interface Liabilities {
  public_debt?: PublicDebt[];
  bank_loans?: BankLoan[];
  private_loans?: PrivateLoan[];
}

export enum IncomeCategory {
  field_1 = '1',
  field_2 = '2',
  field_3 = '3',
  field_4 = '4',
  field_5 = '5',
}

export enum IncomeCategoryWithNoDijazas {
  DIJAZAS_NELKULI = 'díjazás nélküli',
  field_1 = '1',
  field_2 = '2',
  field_3 = '3',
  field_4 = '4',
  field_5 = '5',
}

export interface PastRolesAndAffiliations {
  name: string;
  role: string;
  income_category: IncomeCategoryWithNoDijazas;
}

export interface OngoingIncomeGeneratingActivity {
  name: string;
  income_category: IncomeCategory;
}

export interface HighValueOccasionalIncomeItem {
  name: string;
  income_category: IncomeCategory;
}

export interface Income {
  past_roles_and_affiliations?: PastRolesAndAffiliations[];
  ongoing_income_generating_activities?: OngoingIncomeGeneratingActivity[];
  high_value_occasional_income?: HighValueOccasionalIncomeItem[];
}

export interface OngoingCorporateAndTrustAffiliation {
  organization: string;
  role: string;
  income_category: IncomeCategoryWithNoDijazas;
}

export interface PoliticallyRelevantAndControllingBusinessInterest {
  organization: string;
  role: string;
  ownership_percentage?: string;
  income_category: IncomeCategoryWithNoDijazas;
}

export interface EconomicInterests {
  ongoing_corporate_and_trust_affiliations?: OngoingCorporateAndTrustAffiliation[];
  politically_relevant_and_controlling_business_interests?: PoliticallyRelevantAndControllingBusinessInterest[];
}

export interface Wealth {
  person: Person;
  assets: Assets;
  liabilities: Liabilities;
  income: Income;
  economic_interests: EconomicInterests;
}

export interface WealthView extends Wealth {
  person: PersonView;

  total_real_estate_count: number;
  total_vehicle_count: number;
  total_artwork_count: number;
  total_security_count: number;
  total_income_count: number;
  total_savings: number;
  total_liabilities: number;
  net_worth: number;
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
