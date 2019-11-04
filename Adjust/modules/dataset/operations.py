from django.db.models import Q, Sum, ExpressionWrapper, FloatField


class Operations:
    """
    supports the operations to be made on a dataset
    """
    def __init__(self, date_from, date_to, channels, countries, os, aggregation_list, group_by, order_by):
        """
        init function for the operation object
        :param date_from: the date from which to start filtering to :str
        :param date_to: the date till which filter to :str
        :param channels: the channels for which to filter too :list(str)
        :param countries: the countries for which to filter too :list(str)
        :param os: the os for which to filter too :list(str)
        :param aggregation_list: list of columns for which to perform a sum :list(str)
        :param group_by: list of columns for which to perform a group by :list(str)
        :param order_by: column for which to order by :str (-col_name --> DESC, col_name-->ASC)
        """
        self.date_from = date_from
        self.date_to = date_to
        self.channels = channels
        self.countries = countries
        self.os = os
        self.aggregation_list = aggregation_list
        self.group_by = group_by
        self.order_by = order_by

    def is_empty_query(self):
        """
        checks if the object has been called with an empty query (/dataset)
        :return: true if the query is empty, false otherwise :bool
        """
        if not self.date_from and not self.date_to and not self.channels and not self.countries \
                and not self.os and not self.aggregation_list and not self.group_by and not self.order_by:
            return True
        else:
            return False

    def get_filters(self):
        """
        creates a list of Q objects filters based on the query filters of the object
        :return: the requested list of filters :list(Q())
        """
        filters = list()

        if self.date_from and self.date_to:
            filters.append(Q(date__range=[self.date_from, self.date_to]))
        elif self.date_from and not self.date_to:
            filters.append(Q(date__gte=self.date_from))
        elif not self.date_from and self.date_to:
            filters.append(Q(date__lte=self.date_to))

        if self.channels:
            filters.append(Q(channel__in=self.channels))
        if self.countries:
            filters.append(Q(country__in=self.countries))
        if self.os:
            filters.append(Q(os__in=self.os))

        return filters

    @staticmethod
    def apply_filters(dataset, filters):
        """
        applies the selected filters to a dataset
        :param dataset: the dataset to which to apply the filters to
        :param filters: a list of filters to apply :list(Q())
        :return: the modified dataset
        """
        if len(filters) > 0:
            dataset = dataset.filter(*filters)
        return dataset

    def apply_group_by(self, dataset):
        """
        applies the group by options if selected
        :param dataset: the dataset to which to apply the group by to
        :return: the modified dataset
        """
        if self.group_by:
            dataset = dataset.values(*self.group_by)
        return dataset

    def apply_order_by(self, dataset):
        """
        applies the order by options if selected
        :param dataset: the dataset to which to apply the order by to
        :return: the modified dataset
        """
        if self.order_by:
            dataset = dataset.order_by(self.order_by)
        return dataset

    def apply_aggregation(self, dataset):
        """
        applies the aggregation options if selected. it applies the SUM operator
        :param dataset: the dataset to which to apply the aggregation to
        :return: the modified dataset
        """
        if self.aggregation_list:
            for aggregator in self.aggregation_list:
                if aggregator == 'impressions':
                    dataset = dataset.annotate(impressions=Sum('impressions'))
                if aggregator == 'clicks':
                    dataset = dataset.annotate(clicks=Sum('clicks'))
                if aggregator == 'installs':
                    dataset = dataset.annotate(installs=Sum('installs'))
                if aggregator == 'spend':
                    dataset = dataset.annotate(spend=Sum('spend'))
                if aggregator == 'revenue':
                    dataset = dataset.annotate(revenue=Sum('revenue'))
                if aggregator == 'cpi':
                    dataset = dataset.annotate(cpi=ExpressionWrapper(
                        Sum('spend') / Sum('installs'), output_field=FloatField()))
        return dataset
