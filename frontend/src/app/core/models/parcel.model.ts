export interface LandParcel {
  parcel_id: string;
  khasra_no: string;
  project_id: number;
  project_code: string;
  project_name: string;
  village: string;
  district: string;
  state: string;
  khatedar_owner: string;
  land_category: string;
  area_ha: number;
  acquisition_stage: string;
  dispute_status: string;
  compensation_status: string;
  compensation_amount_lakhs: number;
  risk_level: 'HIGH' | 'MEDIUM' | 'LOW';
  predicted_delay_days: number;
}
