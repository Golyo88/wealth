import { Component, EventEmitter, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { WealthFilters } from '../../models/wealth.model';

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
export class WealthFilterComponent {
  @Output() filterChange = new EventEmitter<WealthFilters>();

  isExpanded = false;
  filters: WealthFilters = {
    order_direction: 'asc',
  };

  counters: CounterFilter[] = [
    {
      label: 'Ingatlanok',
      opKey: 'real_estates_count_op',
      valueKey: 'real_estates_count',
    },
    {
      label: 'Járművek',
      opKey: 'vehicles_count_op',
      valueKey: 'vehicles_count',
    },
    {
      label: 'Értékpapírok',
      opKey: 'securities_count_op',
      valueKey: 'securities_count',
    },
    { label: 'Jövedelmek', opKey: 'income_count_op', valueKey: 'income_count' },
    {
      label: 'Megtakarítások',
      opKey: 'savings_amount_op',
      valueKey: 'savings_amount',
    },
    {
      label: 'Tartozások',
      opKey: 'liabilities_amount_op',
      valueKey: 'liabilities_amount',
    },
    { label: 'Egyenleg', opKey: 'net_worth_op', valueKey: 'net_worth' },
  ];

  toggleFilters() {
    this.isExpanded = !this.isExpanded;
  }

  applyFilters() {
    this.filterChange.emit(this.filters);
  }

  resetFilters() {
    this.filters = { order_direction: 'asc' };
    this.filterChange.emit(this.filters);
  }
}
