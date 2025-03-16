import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import {
  Wealth,
  PaginatedResponse,
  WealthFilters,
  WealthView,
} from '../models/wealth.model';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root',
})
export class WealthService {
  private apiUrl = `${environment.apiUrl}/api`;

  constructor(private http: HttpClient) {}

  getWealths(
    page: number = 1,
    pageSize: number = 10,
    filters?: WealthFilters
  ): Observable<PaginatedResponse<WealthView>> {
    let params = new HttpParams()
      .set('page', page.toString())
      .set('page_size', pageSize.toString());

    if (filters) {
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== undefined && value !== null && value !== '') {
          params = params.set(key, value.toString());
        }
      });
    }

    return this.http.get<PaginatedResponse<WealthView>>(
      `${this.apiUrl}/wealths`,
      {
        params,
      }
    );
  }

  findById(id: string): Observable<WealthView> {
    return this.http.get<WealthView>(`${this.apiUrl}/people/${id}/wealth`);
  }
}
