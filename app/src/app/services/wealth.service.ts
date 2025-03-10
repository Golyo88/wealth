import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import {
  Wealth,
  PaginatedResponse,
  WealthFilters,
} from '../models/wealth.model';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root',
})
export class WealthService {
  private apiUrl = `${environment.apiUrl}/api`;

  constructor(private http: HttpClient) {}

  searchWealth(
    prompt: string,
    page: number = 1,
    pageSize: number = 10
  ): Observable<PaginatedResponse<Wealth>> {
    const params = new HttpParams()
      .set('prompt', prompt)
      .set('page', page.toString())
      .set('page_size', pageSize.toString());

    return this.http.get<PaginatedResponse<Wealth>>(
      `${this.apiUrl}/query/openai`,
      { params }
    );
  }

  findById(id: string): Observable<Wealth> {
    return this.http.get<Wealth>(`${this.apiUrl}/wealths/${id}`);
  }

  getWealths(
    page: number = 1,
    pageSize: number = 10,
    filters?: WealthFilters
  ): Observable<PaginatedResponse<Wealth>> {
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

    return this.http.get<PaginatedResponse<Wealth>>(`${this.apiUrl}/wealths`, {
      params,
    });
  }
}
