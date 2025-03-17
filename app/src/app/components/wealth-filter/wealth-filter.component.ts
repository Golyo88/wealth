import { Component, EventEmitter, Output, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { WealthFilters } from '../../models/wealth.model';
import { Router, ActivatedRoute } from '@angular/router';

interface CounterFilter {
  label: string;
  opKey: keyof WealthFilters;
  valueKey: keyof WealthFilters;
}

@Component({
  selector: 'app-wealth-filter',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './wealth-filter.component.html',
  styleUrls: ['./wealth-filter.component.scss'],
})
export class WealthFilterComponent implements OnInit {
  @Output() filterChange = new EventEmitter<WealthFilters>();

  isExpanded = false;
  filters: WealthFilters = {
    order_direction: 'asc',
  };

  counters: CounterFilter[] = [
    {
      label: 'Ingatlanok száma',
      opKey: 'real_estates_count_op',
      valueKey: 'real_estates_count',
    },
    {
      label: 'Járművek száma',
      opKey: 'vehicles_count_op',
      valueKey: 'vehicles_count',
    },
    {
      label: 'Értékpapírok száma',
      opKey: 'securities_count_op',
      valueKey: 'securities_count',
    },
    {
      label: 'Jövedelmek száma',
      opKey: 'income_count_op',
      valueKey: 'income_count',
    },
    {
      label: 'Megtakarítások összege',
      opKey: 'savings_amount_op',
      valueKey: 'savings_amount',
    },
    {
      label: 'Tartozások összege',
      opKey: 'liabilities_amount_op',
      valueKey: 'liabilities_amount',
    },
    { label: 'Egyenleg', opKey: 'net_worth_op', valueKey: 'net_worth' },
  ];

  constructor(private router: Router, private route: ActivatedRoute) {}

  ngOnInit() {
    this.route.queryParams.subscribe((params) => {
      if (Object.keys(params).length > 0) {
        this.filters = { order_direction: 'asc', ...params };
        sessionStorage.setItem('wealthFilters', JSON.stringify(this.filters));
      } else {
        const savedFilters = sessionStorage.getItem('wealthFilters');
        if (savedFilters) {
          this.filters = JSON.parse(savedFilters);
          this.router.navigate([], {
            relativeTo: this.route,
            queryParams: this.filters,
            queryParamsHandling: 'merge',
          });
        }
      }
      this.filterChange.emit(this.filters);
    });
  }

  toggleFilters() {
    this.isExpanded = !this.isExpanded;
  }

  applyFilters() {
    sessionStorage.setItem('wealthFilters', JSON.stringify(this.filters));
    this.router.navigate([], {
      relativeTo: this.route,
      queryParams: this.filters,
      queryParamsHandling: 'merge',
    });
    this.filterChange.emit(this.filters);
  }

  resetFilters() {
    this.filters = { order_direction: 'asc' };
    sessionStorage.removeItem('wealthFilters');
    this.router.navigate([], {
      relativeTo: this.route,
      queryParams: {},
    });
    this.filterChange.emit(this.filters);
  }
}
