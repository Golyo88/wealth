import { Component, OnInit } from '@angular/core';
import { WealthService } from '../../services/wealth.service';
import {
  Wealth,
  PaginatedResponse,
  Security,
  WealthFilters,
} from '../../models/wealth.model';
import { Subject, debounceTime, distinctUntilChanged } from 'rxjs';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { DecimalPipe } from '@angular/common';
import { Liabilities } from '../../models/wealth.model';
import { WealthFilterComponent } from '../wealth-filter/wealth-filter.component';

@Component({
  selector: 'app-wealth-list',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    FormsModule,
    DecimalPipe,
    WealthFilterComponent,
  ],
  templateUrl: './wealth-list.component.html',
  styleUrls: ['./wealth-list.component.scss'],
})
export class WealthListComponent implements OnInit {
  wealthList: Wealth[] = [];
  loading = false;
  currentPage = 1;
  pageSize = 10;
  totalItems = 0;
  totalPages = 0;
  currentFilters: WealthFilters = {};

  constructor(private wealthService: WealthService) {}

  ngOnInit() {
    this.loadWealths();
  }

  loadWealths() {
    this.loading = true;
    this.wealthService
      .getWealths(this.currentPage, this.pageSize, this.currentFilters)
      .subscribe({
        next: (response) => {
          this.wealthList = response.results;
          this.totalItems = response.pagination.total;
          this.totalPages = response.pagination.total_pages;
        },
        error: (error) => {
          console.error('Hiba történt:', error);
        },
        complete: () => {
          this.loading = false;
        },
      });
  }

  onFiltersChange(filters: WealthFilters) {
    this.currentFilters = filters;
    this.currentPage = 1;
    this.loadWealths();
  }

  onPageChange(page: number) {
    this.currentPage = page;
    this.loadWealths();
  }

  calculateSavings(wealth: Wealth): number {
    // Sum the bank_balance_huf and cash_huf Plust the foreign currency * the exchange rate
    return (
      (wealth.assets.securities?.reduce(
        (sum: number, security: Security) => sum + (security.value_huf || 0),
        0
      ) || 0) +
      (wealth.assets.savings?.deposit_huf || 0) +
      (wealth.assets.savings?.bank_balance_huf || 0) +
      (wealth.assets.savings?.cash_huf || 0) +
      (wealth.assets.savings?.bank_balance_foreign_currency || 0) *
        (wealth.assets.savings?.exchange_rate || 0)
    );
  }

  calculateDebts(wealth: Wealth): number {
    return (
      (wealth.liabilities?.public_debt_huf || 0) +
      (wealth.liabilities?.bank_loans_huf || 0) +
      (wealth.liabilities?.private_loans_huf || 0)
    );
  }

  calculateBalance(wealth: Wealth): number {
    return this.calculateSavings(wealth) - this.calculateDebts(wealth);
  }
}
