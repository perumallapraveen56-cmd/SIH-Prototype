import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

import { ProjectSummary, ProjectDetail } from '../models/project.model';
import { DashboardKPISummary, ProjectRiskOverviewChart } from '../models/risk.model';
import { ProjectGISMarker, GISFilterOptions } from '../models/gis.model';
import { ShapExplanationResponse } from '../models/shap.model';
import { RecommendationListResponse } from '../models/recommendation.model';
import { WhatIfRequest, WhatIfResponse, FinancialImpactResponse } from '../models/whatif.model';
import { AlertItem, AlertPollResponse } from '../models/alert.model';
import { ReportGenerateRequest } from '../models/report.model';
import { LandParcel } from '../models/parcel.model';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private readonly baseUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  private getHeaders(): HttpHeaders {
    const token = localStorage.getItem('sih26017_token');
    let headers = new HttpHeaders({ 'Content-Type': 'application/json' });
    if (token) {
      headers = headers.set('Authorization', `Bearer ${token}`);
    }
    return headers;
  }

  // Dashboard & Analytics
  public getDashboardKPIs(): Observable<DashboardKPISummary> {
    return this.http.get<DashboardKPISummary>(`${this.baseUrl}/analytics/kpis`, { headers: this.getHeaders() });
  }

  public getRiskOverviewChart(): Observable<ProjectRiskOverviewChart> {
    return this.http.get<ProjectRiskOverviewChart>(`${this.baseUrl}/analytics/risk-overview`, { headers: this.getHeaders() });
  }

  // Projects
  public getProjects(filter?: { state?: string; district?: string; project_type?: string; risk_level?: string }): Observable<ProjectSummary[]> {
    let params = new HttpParams();
    if (filter?.state) params = params.set('state', filter.state);
    if (filter?.district) params = params.set('district', filter.district);
    if (filter?.project_type) params = params.set('project_type', filter.project_type);
    if (filter?.risk_level) params = params.set('risk_level', filter.risk_level);

    return this.http.get<ProjectSummary[]>(`${this.baseUrl}/projects`, { headers: this.getHeaders(), params });
  }

  public getProjectDetail(id: number): Observable<ProjectDetail> {
    return this.http.get<ProjectDetail>(`${this.baseUrl}/projects/${id}`, { headers: this.getHeaders() });
  }

  // GIS Risk Map
  public getGisMarkers(filter?: { state?: string; district?: string; project_type?: string; risk_level?: string }): Observable<ProjectGISMarker[]> {
    let params = new HttpParams();
    if (filter?.state) params = params.set('state', filter.state);
    if (filter?.district) params = params.set('district', filter.district);
    if (filter?.project_type) params = params.set('project_type', filter.project_type);
    if (filter?.risk_level) params = params.set('risk_level', filter.risk_level);

    return this.http.get<ProjectGISMarker[]>(`${this.baseUrl}/gis/projects`, { headers: this.getHeaders(), params });
  }

  public getGisFilters(): Observable<GISFilterOptions> {
    return this.http.get<GISFilterOptions>(`${this.baseUrl}/gis/filters`, { headers: this.getHeaders() });
  }

  // SHAP Explainability
  public getShapAnalysis(projectId: number): Observable<ShapExplanationResponse> {
    return this.http.get<ShapExplanationResponse>(`${this.baseUrl}/projects/${projectId}/shap`, { headers: this.getHeaders() });
  }

  // Recommendations & What-If Simulator
  public getRecommendations(projectId: number): Observable<RecommendationListResponse> {
    return this.http.get<RecommendationListResponse>(`${this.baseUrl}/projects/${projectId}/recommendations`, { headers: this.getHeaders() });
  }

  public runWhatIfSimulation(projectId: number, request: WhatIfRequest): Observable<WhatIfResponse> {
    return this.http.post<WhatIfResponse>(`${this.baseUrl}/projects/${projectId}/what-if`, request, { headers: this.getHeaders() });
  }

  public getFinancialImpact(projectId: number): Observable<FinancialImpactResponse> {
    return this.http.get<FinancialImpactResponse>(`${this.baseUrl}/projects/${projectId}/financial-impact`, { headers: this.getHeaders() });
  }

  // Alerts & Notifications
  public getAlerts(severity?: string): Observable<AlertItem[]> {
    let params = new HttpParams();
    if (severity) params = params.set('severity', severity);
    return this.http.get<AlertItem[]>(`${this.baseUrl}/alerts`, { headers: this.getHeaders(), params });
  }

  public pollAlerts(): Observable<AlertPollResponse> {
    return this.http.get<AlertPollResponse>(`${this.baseUrl}/alerts/poll`, { headers: this.getHeaders() });
  }

  public acknowledgeAlert(alertId: string, acknowledgedBy: string): Observable<AlertItem> {
    return this.http.post<AlertItem>(
      `${this.baseUrl}/alerts/${alertId}/acknowledge`,
      { acknowledged_by: acknowledgedBy },
      { headers: this.getHeaders() }
    );
  }

  public triggerLiveAlert(projectId?: number): Observable<AlertItem> {
    let params = new HttpParams();
    if (projectId) params = params.set('project_id', projectId);
    return this.http.post<AlertItem>(`${this.baseUrl}/alerts/trigger-live`, {}, { headers: this.getHeaders(), params });
  }

  // Reports
  public generateReport(request: ReportGenerateRequest): Observable<any> {
    if (request.export_format?.toLowerCase() === 'pdf') {
      return this.http.post(`${this.baseUrl}/reports/generate`, request, {
        headers: this.getHeaders(),
        responseType: 'blob' as 'json'
      });
    }
    return this.http.post(`${this.baseUrl}/reports/generate`, request, { headers: this.getHeaders() });
  }

  public downloadProjectReportPdf(projectId: number): Observable<Blob> {
    return this.http.get(`${this.baseUrl}/reports/download-pdf/${projectId}`, {
      headers: this.getHeaders(),
      responseType: 'blob'
    });
  }

  public downloadProjectReportPdfUrl(projectId: number): string {
    return `${this.baseUrl}/reports/download-pdf/${projectId}`;
  }

  // Land Parcels
  public getLandParcels(filter?: { projectId?: number; stage?: string; disputeStatus?: string }): Observable<LandParcel[]> {
    let params = new HttpParams();
    if (filter?.projectId) params = params.set('project_id', filter.projectId);
    if (filter?.stage) params = params.set('stage', filter.stage);
    if (filter?.disputeStatus) params = params.set('dispute_status', filter.disputeStatus);

    return this.http.get<LandParcel[]>(`${this.baseUrl}/projects/parcels/all`, { headers: this.getHeaders(), params });
  }
}
