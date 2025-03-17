import { Component, OnInit } from '@angular/core';
import { WealthService } from '../../services/wealth.service';
import {
  Wealth,
  PaginatedResponse,
  Security,
  WealthFilters,
  WealthView,
} from '../../models/wealth.model';
import { Subject, debounceTime, distinctUntilChanged } from 'rxjs';
import { CommonModule } from '@angular/common';
import { RouterModule, ActivatedRoute } from '@angular/router';
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
  wealthList: WealthView[] = [];
  loading = false;
  currentPage = 1;
  pageSize = 10;
  totalItems = 0;
  totalPages = 0;
  currentFilters: WealthFilters = {};

  constructor(
    private wealthService: WealthService,
    private route: ActivatedRoute
  ) {}

  ngOnInit() {
    this.route.queryParams.subscribe((params) => {
      if (Object.keys(params).length > 0) {
        this.currentFilters = params;
      }
      this.loadWealths();
    });
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
}
